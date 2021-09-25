import os
from flask_pymongo import pymongo

MONGO_URI = os.environ.get('MONGO_URI')

def get_tenant(tenant):
    client = pymongo.MongoClient(MONGO_URI + tenant)
    return client.get_database()