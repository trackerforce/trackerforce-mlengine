from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
from utils import parse_json 

import controller

flask_app = Flask(__name__)

@flask_app.route('/check', methods=['GET'])
def check():
    return parse_json({ 'result': 'All good' })

@flask_app.route('/train/v1/<tenant>', methods=['POST'])
def train_handler(tenant):
    try:
        return controller.on_train(tenant, request.get_json())
    except Exception as e:
        print(e)
        return parse_json({ 'error': 'Something went wrong' })

@flask_app.route('/predict/v1/<tenant>', methods=['POST'])
def predict_handler(tenant):
    try:
        return controller.on_predict(tenant, request.get_json())
    except Exception as e:
        print(e)
        return parse_json({ 'error': 'Something went wrong' })

if __name__ == "__main__":
  flask_app.run()