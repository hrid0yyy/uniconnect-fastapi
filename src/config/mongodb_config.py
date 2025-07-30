from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection setup
client = MongoClient(os.getenv("MONGO_URI")) 

def get_collection(db_name: str, collection_name: str):
    """
    Get a specific collection from the database.
    """
    return client[db_name][collection_name]
    