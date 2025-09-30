from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from the .env file
load_dotenv()

# MongoDB setup using environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for the response data structure
class CollectibleItem(BaseModel):
    id: str
    name: str
    price: str
    image: str
    url: str
    saved: bool

# Endpoint to fetch all items from MongoDB
@app.get("/items", response_model=List[CollectibleItem])
def get_items():
    """
    Fetches all collectible items from the database.
    """
    items = collection.find()
    items_list = [
        CollectibleItem(
            id=str(item["_id"]),
            name=item["title"],
            price=item["price"],
            image=item["image"],
            url=item["link"],
            saved=item["like"]
        )
        for item in items
    ]
    return items_list

# Endpoint to update the "saved" status of an item
@app.put("/items/{item_id}", response_model=CollectibleItem)
def update_item(item_id: str, saved: bool):
    """
    Updates the saved status of an item based on its ID.
    """
    result = collection.update_one(
        {"_id": item_id},
        {"$set": {"like": saved}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = collection.find_one({"_id": item_id})
    return CollectibleItem(
        id=str(item["_id"]),
        name=item["title"],
        price=item["price"],
        image=item["image"],
        url=item["link"],
        saved=item["like"]
    )

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
