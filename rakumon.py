import google.generativeai as genai
import typing_extensions as typing
import ast
from PIL import Image
import numpy as np
import torch
import requests
import json
import os
import time

gemini_api = "AIzaSyDm405ADxMiDWho-n1BrZX6xiuCGSZm1oc"
genai.configure(api_key=gemini_api)

#-----------------------------This Will Talk To User--------------------------#
def create_rakumon_model(user_details):

    class ChatbotOutput(typing.TypedDict):
        message_to_user: str
        database_required: bool
        window_shopping: bool
        user_of_product_description: str  # typing.Optional[P]

    user_of_product_description = "user of product: gender (example: Kid, Girl/Boy, Men/Women), persona (example: gamer, techie, travel, fashion, cooking, etc) "

    instruction = (
        f"You are a chatbot shopkeeper. Your name is Rakumon and always call User with a nickname. Details about User are: {user_details}. You will talk in funny, sarcastic, "
        "interesting way to the user and in the same language as of the user. You will always answer in json format as I have given. "
        "I have a database of ecommerce products. So, You have 2 works to do. "
        "First, if user just talking to you or asking a simple query in which there is no requirement of database, "
        "in that case just talk back to the user, database_required will be False. "
        "Second, If user is asking anything related to ecommerce products, you have to answer back plus also have to tell me "
        "that database_required is True and in the user_of_product_description, only give the detailed user_of_product_description (comma separated) that user has given. "
        "If user has not given anything about the user of the product, give user details as given in the user_of_product_description. "
        "Do not provide gender if it is not required for the product, such as in categories like Kitchen, Tools, Books, Hardware, etc. Provide gender information only when it is relevant for product search. "
        f"user_of_product_description must be in this exact same format: {user_of_product_description}. "
        "If user is confused or want to do window shopping or want something random, make window_shopping True otherwise it will be False. "
        "Keep in mind that you ask less questions so that the user is not irritated. Rather try to understand his preference from history and chat."
    )

    # Using `response_mime_type` with `response_schema` requires a Gemini 1.5 Pro model
    model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  system_instruction=instruction,
                                  # Set the `response_mime_type` to output JSON
                                  # Pass the schema object to the `response_schema` field
                                  generation_config={"response_mime_type": "application/json",
                                                     "response_schema": ChatbotOutput})

    return model

def gemini_response(user_message, user_details, history):
    url = "http://127.0.0.1:5500/query"
    # Define the query data to send
    data = {
        "user_message": user_message,
        "user_details": user_details,
        "history": history
    }
    # Send the POST request
    response = requests.post(url, json=data)
    gemini_json = json.loads(response.text)
    return gemini_json
#-----------------------------Window shopping System--------------------------#

def window_shopping_model():

    class BotOutput(typing.TypedDict):
        generated_query: str

    product_description = "product, category, title, color, description by given by the user, age of customer of that product if given"

    instruction = (
        "I will provide you user_message and user_details. As the user is confused or want to do window shopping or want something random, "
        f"just use user_details to create a generated_query which is basically a product description (comma separated) in this format - {product_description}. "
        "I will use this generated_query to search in vectorDB of products."
    )

    # Using `response_mime_type` with `response_schema` requires a Gemini 1.5 Pro model
    model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  system_instruction=instruction,
                                  # Set the `response_mime_type` to output JSON
                                  # Pass the schema object to the `response_schema` field
                                  generation_config={"response_mime_type": "application/json",
                                                     "response_schema": BotOutput})

    return model


def query_for_window_shopping(user_details, user_message):
    model = window_shopping_model()
    query_response = model.generate_content([f"user_details: {user_details}, user_message: {user_message}"])
    query = json.loads(query_response.text)['generated_query']
    return query

#-----------------------------Query Restructuring with Retrieval of Products (Mistral AI)--------------------------#

def retrieve_products_with_query_restructuring(user_of_product_description, user_message):
    url = "http://127.0.0.1:9000/query"
    prompt = f"{user_message} {user_of_product_description}"
    # Define the query data to send
    data = {
        "prompt": prompt
    }
    # Send the POST request
    response = requests.post(url, json=data)
    products_json = json.loads(response.text)
    return products_json["results"]



#-----------------------------AG Part Of RAG System--------------------------#

def reader_rag_model():

    class BotOutput(typing.TypedDict):
        product_description: str

    instruction = (
        "You are a shopkeeper of ecommerce platform and your name is Rakumon. I will be providing you user details, user query and the products details. "
        "You have to augment the product details and generate a small product description (20 words) in a user personalized manner. "
        "Basically, create a 20 words product description that highlights the features and aspects that users are most likely to prefer. "
        "Product details will have things about product like title, category, features and I will also give image of the product. "
        "Give in json format as I have given. "
    )

    # Using `response_mime_type` with `response_schema` requires a Gemini 1.5 Pro model
    model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  system_instruction=instruction,
                                  # Set the `response_mime_type` to output JSON
                                  # Pass the schema object to the `response_schema` field
                                  generation_config={"response_mime_type": "application/json",
                                                     "response_schema": BotOutput})

    return model

#----------------------------R (Retrieval) Part Of RAG System-----------------------#

def retrieve_products(query):
    url = "http://127.0.0.1:5001/query"

    # Define the query data to send
    data = {
        "query": query
    }
    # Send the POST request
    response = requests.post(url, json=data)
    products_json = json.loads(response.text)
    return products_json["results"]

#------------------------Full Process of RAG System---------------------------------#

def generate_products_with_rag_v2(user_product_description, user_details, user_message):
    products = []
    products_list = retrieve_products_with_query_restructuring(user_product_description, user_message)
    reader = reader_rag_model()
    #####
    for product in products_list:
        product_details = {
            "title": product["Metadata"]["title"],
            'features': product["Metadata"]['product_features']
        }
        query = f"user_query:{user_message}, user_details: {user_details}, product_details: {product_details}"
        img = Image.open(requests.get(product["Metadata"]["image_url"], stream=True).raw)
        desc_response = reader.generate_content([query, img]) # description response
        product_description = json.loads(desc_response.text)['product_description']
        products.append({
            "product_img_url": product["Metadata"]["image_url"],
            "product_title": product["Metadata"]["title"],
            "product_description": product_description,
            "product_price": f"${product['Metadata']['price']}"
        })
    #####
    return products

def generate_products_with_rag(user_product_description, user_details, user_message):
    products = []
    products_list = retrieve_products(user_product_description)
    reader = reader_rag_model()
    #####
    for product in products_list:
        product_details = {
            "title": product["Metadata"]["title"]
        }
        query = f"user_query:{user_message}, user_details: {user_details}, product_details: {product_details}"
        img = Image.open(requests.get(product["Metadata"]["image_url"], stream=True).raw)
        desc_response = reader.generate_content([query, img]) # description response
        product_description = json.loads(desc_response.text)['product_description']
        products.append({
            "product_img_url": product["Metadata"]["image_url"],
            "product_title": product["Metadata"]["title"],
            "product_description": product_description,
            "product_price": f"${product['Metadata']['price']}"
        })
    #####
    return products


#------------------------Full Process of Rakumon-------------------------------------#

def generate_rakumon_response(user_message, user_details, history_data):
    history = history_data['history']
    bot = gemini_response(user_message, user_details, history) # Gemini Server
    #####
    if len(history_data['history']) >=6: # if 3 chats are done (2 * 3 = 6)
        history_data['history'] = history_data['history'][2:] # remove first user-model pair
    history_data['history'].append({
        'role': 'user',
        'parts': user_message
    })
    #####
    response_dict = {}
    print(bot)
    response_dict["message_to_user"] = bot['message_to_user']
    print("rakumon responded")
    try:
        if bot['database_required'] == False:
            response_dict["products_are_produced"] = False
            history_data['history'].append({
                'role': 'model',
                'parts': bot['message_to_user']
            })
        else:
            try:
                if bot['window_shopping'] == True:
                    user_product_description = query_for_window_shopping(user_details, user_message)
                else:
                    user_product_description = bot['user_of_product_description']
            except:
                user_product_description = bot['user_of_product_description']
            print("generated query: ", user_product_description)
            print("rakumon send message to rag")
            # products = generate_products_with_rag(user_product_description, user_details, user_message)
            products = generate_products_with_rag_v2(user_product_description, user_details, user_message)
            response_dict["products_are_produced"] = True
            response_dict["products"] = products
            # product_data = {f"product_{i}":{"title":products[i]["product_title"],"description":products[i]["product_description"],"price":products[i]["product_price"]} for i in range(len(products))}
            history_data['history'].append({
                'role': 'model',
                'parts': f"{bot['message_to_user']}" #, {product_data}"
            })
            print("process completed")
    except:
        response_dict["products_are_produced"] = False
        history_data['history'].append({
            'role': 'model',
            'parts': bot['message_to_user']
        })
    #####

    return history_data, response_dict
