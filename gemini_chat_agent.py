import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import typing_extensions as typing

app = FastAPI()
# Please contact 21je0918@iitism.ac.in incase you face any issue.

gemini_api = "YOUR_GEMINI_API"
genai.configure(api_key=gemini_api)


class QueryRequest(BaseModel):
    user_message: str
    user_details: dict
    history: list


def generate_rakumon_response(user_message: str, user_details: dict, history: dict):

    class ChatbotOutput(typing.TypedDict):
        message_to_user: str
        database_required: bool
        window_shopping: bool
        user_of_product_description: str

    user_of_product_description = "user of product: gender (example: Kid, Girl/Boy, Men/Women), persona (example: gamer, techie, travel, cooking, etc)"

    instruction = (
        f"You are a chatbot shopkeeper. Your name is Rakumon and always call User with a nickname. Details about User are: {user_details}. You will talk in funny, sarcastic, "
        "interesting way to the user and in the same language as of the user. You will always answer in json format as I have given. "
        "I have a database of ecommerce products. So, You have 2 works to do. "
        "First, if user just talking to you or asking a simple query in which there is no requirement of database, "
        "in that case just talk back to the user, database_required will be False. "
        "Second, If user is asking anything related to ecommerce products, you have to answer back plus also have to tell me "
        "that database_required is True and in the user_of_product_description, only give the detailed user_of_product_description (comma separated) that user has given. "
        "If user has not given anything about the user of the product, give user details as given in the user_of_product_description. "
        "Make user_of_product_description empty if and only if it is not required for the product, such products can be in these categories - Kitchen, Tools, Books, Hardware, etc. Provide user_of_product_description only when it is relevant for product search. "
        f"user_of_product_description must be in this exact same format: {user_of_product_description}. "
        "If user is confused or want to do window shopping or want something random, make window_shopping True otherwise it will be False. "
        "Keep in mind that you ask less questions so that the user is not irritated. Rather try to understand his preference from history and chat."
    )

    # Using `response_mime_type` with `response_schema` requires a Gemini 1.5 Pro model
    rakumon_model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  system_instruction=instruction,
                                  # Set the `response_mime_type` to output JSON
                                  # Pass the schema object to the `response_schema` field
                                  generation_config={"response_mime_type": "application/json",
                                                     "response_schema": ChatbotOutput})

    try:
        rakumon_chat = rakumon_model.start_chat(history=history)
        response = rakumon_chat.send_message(content=[user_message],)

        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in restructuring query: {str(e)}")


@app.post("/query")
async def respond_user_message(request: QueryRequest):
    """Handle requests and return gemini json output. """

    try:
        # First, get gemini response
        gemini_response = generate_rakumon_response(request.user_message, request.user_details, request.history)

        # Check if the gemini_response is in dict format and get the first item
        if isinstance(gemini_response, dict) and gemini_response:
            gemini_json_output = gemini_response
        else:
            raise HTTPException(status_code=500, detail="Invalid format of restructured query.")

        print(gemini_json_output)
        return gemini_json_output
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5500, log_level="info")
