import flask
from flask import Flask, render_template, request, jsonify
import json
import io
from PIL import Image
from huggingface_hub import login
import requests
import shutil
import os
import time
from rakumon import create_rakumon_model, generate_rakumon_response

with open("history.json", 'w') as file:
    json.dump({"history": []}, file, indent=4) # empty chat history before starting app

with open("family_history_with_rakumon.json", 'w') as file:
    json.dump({"history": []}, file, indent=4) # empty family chat history before starting app

app = Flask(__name__)

# Please contact 21je0918@iitism.ac.in or siddharthmishra.work@gmail.com incase you face any issue.
# Please contact 21je0928@iitism.ac.in incase you face any issue.

hf_token = "HUGGINGFACE_API_TOKEN"
login(token=hf_token, add_to_git_credential=True)

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/family')
def family():
    return render_template('family.html')

@app.route('/designer')
def designer():
    return render_template('designer.html')

#--------------------------Rakumon Designer-----------------------------------#

@app.route('/send_message_designer', methods=['POST'])
def send_message_designer():
    user_message = request.form['message']
    response_message = generate_response_designer(user_message)
    return jsonify(response_message)

def creative_image_search(image_path, num): # vectorDB search will be here
    if num == 3: # Pandas
        response = {
            "message_to_user": f"Here are the similar products for image {num}.",
            "images_are_produced": False,
            "products_are_produced": True,
            "products": [
                {
                    "product_img_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTsWH_MsGc90i-YTiv4z0r287osaO5sOOC_5YaOCRliD0IQpp5yVmlOdeNRTK7CMZAxQCIsr5WXOobipIa589OkbDh3TyyIr5vDoiJ3EFitzujxcNCjl8WFaQ&usqp=CAE%27",
                    "product_title": "Cute Panda Light Lamp For Kids",
                    "product_description": "This is a cute lamp for your cute kids.",
                    "product_price": "$19.99"
                },
                {
                    "product_img_url": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTPSLW4vHYsAo1JHeNKBL3vGhr8IZgvX0YoisJlYm1-Jf45QPWe7bQbufR9_oxY3GqCKuQOHppV0o5X3DEDchWkcsOT3dXBcY4pMsTctuBIrn49zNEKRUZGSQ&usqp=CAE%27",
                    "product_title": "Love Craft Gifts Personalized Wooden ",
                    "product_description": "This can be a good gift for your loved ones.",
                    "product_price": "$29.99"
                },
                {
                    "product_img_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRCGLgWo2dodcilKVrAIOKckupt6GGedmWKqSSaC_gvgOGCirIUKGUzPMsoKAEz6hweoCQzpkq00NHVz9b1clgk5mLwdzl1Z9dpZ9iZ5H35G0Zeqephv8HR6w&usqp=CAE%27",
                    "product_title": "Kids animal table lamp",
                    "product_description": "Buy this for your child. It will make your kid happy.",
                    "product_price": "$39.99"
                }
            ]
        }
    elif num == 1: # Vase
        response = {
            "message_to_user": f"Here are the similar products for image {num}.",
            "images_are_produced": False,
            "products_are_produced": True,
            "products": [
                {
                    "product_img_url": "https://m.media-amazon.com/images/I/31LqzOsHtJL._AC_.jpg",
                    "product_title": "Goodthreads Women's High-Rise Chino Girlfriend Short",
                    "product_description": "This is a brief description of Product 1.",
                    "product_price": "$19.99"
                },
                {
                    "product_img_url": "https://m.media-amazon.com/images/I/31LqzOsHtJL._AC_.jpg",
                    "product_title": "Goodthreads Women's High-Rise Chino Girlfriend Short",
                    "product_description": "This is a brief description of Product 2.",
                    "product_price": "$29.99"
                },
                {
                    "product_img_url": "https://m.media-amazon.com/images/I/31LqzOsHtJL._AC_.jpg",
                    "product_title": "Goodthreads Women's High-Rise Chino Girlfriend Short",
                    "product_description": "This is a brief description of Product 3.",
                    "product_price": "$39.99"
                }
            ]
        }
    else:
        response = {
            "message_to_user": f"Here are the similar products for image {num}.",
            "images_are_produced": False,
            "products_are_produced": True,
            "products": [
                {
                    "product_img_url": "https://m.media-amazon.com/images/I/31LqzOsHtJL._AC_.jpg",
                    "product_title": "Goodthreads Women's High-Rise Chino Girlfriend Short",
                    "product_description": "This is a brief description of Product 1.",
                    "product_price": "$19.99"
                },
                {
                    "product_img_url": "https://m.media-amazon.com/images/I/31LqzOsHtJL._AC_.jpg",
                    "product_title": "Goodthreads Women's High-Rise Chino Girlfriend Short",
                    "product_description": "This is a brief description of Product 2.",
                    "product_price": "$29.99"
                },
                {
                    "product_img_url": "https://m.media-amazon.com/images/I/31LqzOsHtJL._AC_.jpg",
                    "product_title": "Goodthreads Women's High-Rise Chino Girlfriend Short",
                    "product_description": "This is a brief description of Product 3.",
                    "product_price": "$39.99"
                }
            ]
        }

    return response

def generate_response_designer(user_message):

    s = user_message.strip()
    try:
        for i in range(3):
            shutil.move(f"./static/images/imgs/img{i}.jpeg", f"./static/images/img{i}.jpeg")
        shutil.rmtree("./static/images/imgs")
    except:
        pass
    os.makedirs("./static/images/imgs", exist_ok=True)
    if s.isdigit():
        if int(s) > 3 or int(s) < 1:
            response = {
                "message_to_user": "Sorry, I cannot help you with that, please try again. If you have general query, please ask to Rakumon.",
                "images_are_produced": False,
                "products_are_produced": False,
            }
        else:
            n = int(s) - 1
            image_path = f'./static/images/img{n}.jpeg'
            response = creative_image_search(image_path, int(s))
    else:
        for i in range(3): # we have to show 3 images
            flag = False
            print("start")
            for j in range(5): # try 5 times for each image if error comes
                image_bytes = query({
                    "inputs": user_message,
                })
                print(type(image_bytes))
                try:
                    user_message += "."
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(f'./static/images/imgs/img{i}.jpeg', format='JPEG')
                    # with open(f'./static/images/img{i}.jpeg', 'wb') as img_file:
                    #     img_file.write(image_bytes)
                    print("image saved")
                    break
                except:
                    if j == 4: # It wasn't able to generate 5th time.
                        flag = True
                        user_message += "."
                        break
                    continue
            if flag:
                break
            print(i, "done")
        if flag:
            response = {
                "message_to_user": "Sorry, I cannot help you with that, please try again. If you have general query, please ask to Rakumon.",
                "images_are_produced": False,
                "products_are_produced": False,
            }
        else:
            response = {
                "message_to_user": "Here are the three images I created for you. Which one do you like the most?",
                "images_are_produced": True,
                "images": [{"designed_image_path": flask.url_for('static', filename=f'images/imgs/img{i}.jpeg') + f'?v={int(time.time())}'} for i in range(3)],
                "products_are_produced": False,
            }
    return response

#--------------------------Rakumon Family-----------------------------------#

@app.route('/send_message_family', methods=['POST'])
def send_message_family():
    user_message = request.form['message']
    response_message = generate_response_family(user_message)
    return jsonify(response_message)

def generate_response_family(user_message):
    ### User
    with open("users.json", 'r') as file:
        data = json.load(file)
    user_details = data['user_id_12']  # From On-boarding process

    with open("family_history_with_rakumon.json", 'r') as file:
        history_data = json.load(file)
    print(history_data)

    #####
    history_data, rakumon_response = generate_rakumon_response(user_message, user_details, history_data)

    with open("family_history_with_rakumon.json", 'w') as file:
        json.dump(history_data, file, indent=4)

    return rakumon_response

#--------------------------Rakumon-----------------------------------#

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response_message = generate_response(user_message)
    return jsonify(response_message)

def generate_response(user_message):
    ### User
    with open("users.json", 'r') as file:
        data = json.load(file)
    user_details = data['user_id_12']  # From On-boarding process

    with open("history.json", 'r') as file:
        history_data = json.load(file)
    print(history_data)

    #####
    history_data, rakumon_response = generate_rakumon_response(user_message, user_details, history_data)

    with open("history.json", 'w') as file:
        json.dump(history_data, file, indent=4)

    return rakumon_response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
