import os
from pymongo import MongoClient
from datetime import datetime

def get_db():
    """Connects to MongoDB and returns the database object."""
    try:
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not set in environment variables")
        client = MongoClient(mongo_uri)
        db = client['recipe-app']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None