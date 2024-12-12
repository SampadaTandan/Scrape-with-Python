from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection string from the .env file
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)

db = client.scrapy

posts = db.book_collection

doc = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

post_id = posts.insert_one(doc).inserted_id

print(f"Inserted document ID: {post_id}")
