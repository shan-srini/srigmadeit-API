import os
from pymongo import MongoClient

database_name = os.environ['DB_NAME']

def get_client():
    return MongoClient(os.environ['MONGO_DB_CONNECT'])

def get_db():
    return get_client()[database_name]