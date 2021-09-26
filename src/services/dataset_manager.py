import pickle
import time
import json

from flask.wrappers import Request
from services import parse_json
from model.dataset import Dataset

class DatasetManager():
    """ Handle Dataset operations such as
        - Validate datasets
        - Create and update datasets
        - Run dataset training
     """

    def __init__(self, tenant_db):
        self._tenant_db = tenant_db

    def find_create_dataset(self, request_body: dict) -> dict:
        dataset = self._tenant_db.datasets.find_one({ 'context_id': request_body['contextId'] })
        if dataset is not None:
            return parse_json(dataset)

        dataset = self.__create_dataset__(request_body)
        return json.loads(dataset.toJSON())

    def insert_example(self, dataset: dict, request_body: dict):
        model = Dataset.__get_model__(dataset['models'], request_body['id'])
        if model is None:
            raise Exception('Model not found')

        sample = Dataset.__prepare_sample__(model, request_body['tasks'])
        # TODO: Retrieve sample collection and insert new sampe
        print(sample)

    def train(self, request: dict):
        pass
    
    def __create_dataset__(self, request_body: dict):
        dataset = Dataset(request = request_body)
        res = self._tenant_db.datasets.insert_one(json.loads(dataset.toJSON()))
        return dataset

    def __save_model_to_db__(self, model, model_name):
        pickled_model = pickle.dumps(model)
        
        info = self._tenant_db.insert_one({ model_name: pickled_model, 'name': model_name, 'created_time': time.time() })
        print(info.inserted_id, ' saved with this id successfully!')
        
        details = {
            'inserted_id': info.inserted_id,
            'model_name': model_name,
            'created_time': time.time()
        }
        
        return details

    def __load_saved_model_from_db__(self, model_name):
        json_data = {}

        data = self._tenant_db.find({ 'name': model_name })
        for i in data:
            json_data = i

        pickled_model = json_data[model_name]
        return pickle.loads(pickled_model)