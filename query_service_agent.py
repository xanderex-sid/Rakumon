import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mistralai import Mistral
from pinecone.grpc import PineconeGRPC as Pinecone
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Initialize Mistral and Pinecone clients
mistral_api_key = "LT4hpqvlFuXXuinglel6XnCmJXQuGjjN"
mistral_model = "mistral-large-latest"  # Adjust to your actual model if needed

pc = Pinecone(api_key='5a9fb6d6-b376-484c-b0b3-c3fbc6d21208')
index = pc.Index('ecom-vectordb') # "product-vectordb"
emb_model = SentenceTransformer('BAAI/bge-m3')

# Example queries for reference
examples = [
    {"user_prompt": "I'm looking for a cozy winter coat that would be perfect for my ski trip. user of product: Women, traveller",
     "restructured_query": "Winter coat for skiing, women"},
    {"user_prompt": "Can you find me a stylish backpack that I can use for college and is good for carrying a laptop? user of product: Male, Techie",
     "restructured_query": "Stylish backpack for college with laptop compartment, Male, Boy, Techie"},
    {"user_prompt": "I need a high-quality blender for making smoothies. It should be easy to clean and durable. user of product: women, cooking",
     "restructured_query": "High-quality blender for smoothies, easy to clean, durable"},
    {"user_prompt": "Show me some unique wall art that would be great for decorating a modern living room. user of product: women, artist",
     "restructured_query": "Unique wall art for modern living room decoration, artist"},
    {"user_prompt": "I want to buy a set of professional kitchen knives. They should be sharp and come with a good storage block. user of product: Women, cooking",
     "restructured_query": "Professional kitchen knife set, sharp, with storage block"},
    {"user_prompt": "Looking for eco-friendly yoga mats that are also extra thick for comfort during long sessions. user of product: yoga, man",
     "restructured_query": "Eco-friendly extra thick yoga mats"},
    {"user_prompt": "Find me a set of elegant dinnerware that includes plates, bowls, and mugs. It should be suitable for formal occasions. user of product: women, party girl",
     "restructured_query": "Elegant dinnerware set with plates, bowls, mugs, for formal occasions"},
    {"user_prompt": "I need a lightweight tent for backpacking that can withstand rain and is easy to set up. user of product: Man, Tracking, Traveller",
     "restructured_query": "Lightweight backpacking tent, rain-resistant, easy setup for men, mountain tracking."},
    {"user_prompt": "Show me some affordable smartwatches that have health tracking features and are compatible with iPhones. user of product: Man, Techie",
     "restructured_query": "Affordable smartwatches with health tracking, iPhone compatible, Digital for Man."},
    {"user_prompt": "I'm searching for a high-quality leather briefcase for work that has enough space for a laptop and documents. user of product: Man, Entrepreneur",
     "restructured_query": "High-quality leather briefcase for work, space for laptop and documents for Man and Entrepreneurs."},
    {"user_prompt": "I'm searching for a high-graphics gaming lenevo laptops. user of product: Man, Gamer, Techie",
     "restructured_query": "High-graphics gaming laptop, lenevo, Gamer, Techie."},
    {"user_prompt": "I want to buy watch for my younger brother of age 13. user of product: Kid",
     "restructured_query": "Stylish Watch, Kid."},
    {"user_prompt": "Frok for a girl of age 16. user of product: Girl, Fashion, Stylish",
     "restructured_query": "Beautiful Frok, Girl, Pretty."}
]

class QueryRequest(BaseModel):
    prompt: str

def query_restructuring(prompt: str) -> str:
    instruction = (
        f"You are a query restructuring agent. You'll be passed a user conversational query prompt about a product with the details of the user of that product. "
        "The user prompt may be multilingual, so keep in mind to translate objects in other languages to their English names. "
        "Your job is to format this prompt into a useful English shopping query. "
        "For age use words only out of these - Kid, Boy, Girl, Men, Women. Don't use numbers for age. "
        "Give restructured query only and only in English. "
        "This shopping query will be used for vector search. "
        f"Here are a few examples:{str(examples)} "
        "Your output is the restructured query only in list format."
    )

    client = Mistral(api_key=mistral_api_key)
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]

    try:
        chat_response = client.chat.complete(
            model=mistral_model,
            messages=messages,
            response_format={
                "type": "json_object"
            }
        )
        response = json.loads(chat_response.choices[0].message.content)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in restructuring query: {str(e)}")

def query_index(query: str):
    """Encode the query, perform a search on the index, and return the results as a JSON object."""
    # Encode the query
    xq = emb_model.encode(query, normalize_embeddings=True).tolist()

    # Perform the query on the index
    xc = index.query(vector=xq, top_k=5, include_metadata=True)

    # Format the results
    results = []
    for result in xc['matches']:  # Adjust this according to the structure of your result
        results.append({
            "ID": result['id'],
            "Score": result['score'],
            "Metadata": result['metadata']
        })

    return {"results": results}


@app.post("/query")
async def perform_query(request: QueryRequest):
    """Handle query requests and return results."""
    try:
        # First, restructure the query
        restructured_query_response = query_restructuring(request.prompt)

        restructured_query = restructured_query_response  # Expecting a list from restructuring function

        # Check if the restructured query is in list format and get the first item
        if isinstance(restructured_query, list) and restructured_query:
            restructured_query = restructured_query[0]
        else:
            raise HTTPException(status_code=500, detail="Invalid format of restructured query.")

        # Then, perform the query on the index with the restructured query
        print(restructured_query)
        results = query_index(restructured_query)
        return results
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000, log_level="info")
