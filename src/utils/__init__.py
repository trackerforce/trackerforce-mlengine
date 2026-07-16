""" Utility functions """
import json
import uuid

from bson import json_util

def parse_json(data):
    """ Parse JSON data """
    return json.loads(json_util.dumps(data))

def generate_id():
    """ Generate a unique identifier """
    return str(uuid.uuid4())
