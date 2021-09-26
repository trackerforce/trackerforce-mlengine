import json

from bson import json_util

from .engine import train_model

def parse_json(data):
    return json.loads(json_util.dumps(data))