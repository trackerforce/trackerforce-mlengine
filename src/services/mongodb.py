import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI')

def get_tenant(tenant):
    client = MongoClient(MONGO_URI + tenant)
    return client.get_database()