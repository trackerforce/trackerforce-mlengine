import os
import json

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
from bson import json_util

import controller

flask_app = Flask(__name__)

@flask_app.route('/check', methods=['GET'])
def check():
    return json.loads(json_util.dumps({ 'result': 'All good' }))

@flask_app.route('/train/v1/<tenant>', methods=['POST'])
def train_handler(tenant):
    return controller.on_train(tenant, request.get_json())

@flask_app.route('/predict/v1/<tenant>', methods=['GET'])
def predict_handler(tenant):
    return controller.on_predict(tenant, request.get_json())

if __name__ == "__main__":
  flask_app.run()