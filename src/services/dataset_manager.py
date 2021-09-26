import pickle
import time
import json

from services import train_model, predict_entry
from model.dataset import Dataset
from utils import parse_json

class DatasetManager():
    """ Handle Dataset operations such as
        - Validate datasets
        - Create and update datasets
        - Run dataset training
     """

    def __init__(self, tenant_db):
        self._tenant_db = tenant_db

    def find_create_dataset(self, request_body: dict) -> dict:
        """ Try to find dataset, if it does not exist, create """
        
        context_id = request_body['contextId']
        dataset = self._tenant_db.datasets.find_one({ 'context_id': context_id })
        if dataset is not None:
            return parse_json(dataset)

        dataset = self.__create_dataset__(request_body)
        return json.loads(dataset.toJSON())

    def insert_example(self, dataset: dict, request_body: dict) -> dict:
        """ Transform sample input and insert it to the dataset collection """

        model_info = Dataset.__get_model__(dataset['models'], request_body['id'])
        if model_info is None:
            raise Exception('Model Info not found')

        sample = Dataset.__prepare_sample__(model_info, request_body['tasks'])
        self.__add_sample_collection__(
            collection=model_info['collection_name'],
            resolution=request_body['resolution'],
            sample=sample,
            model_info=model_info
        )

        return model_info

    def train_update(self, dataset: dict, model_info: dict):
        """ 
            Retrieve samples from the DB and send to the ML engine to train the model.
            Returns the accuracy
        """

        collection = model_info['collection_name']
        samples = self._tenant_db[collection].find({}, { '_id': False })
        
        model, accuracy = train_model(model_info, samples)
        self.__save_model_to_db__(
            dataset=dataset, 
            model_info=model_info,
            model=model, 
            accuracy=accuracy * 100
        )

        return accuracy

    def predict(self, request_body: dict):
        context_id = request_body['contextId']
        procedure_id = request_body['id']

        model, accuracy = self.__load_saved_model_from_db__(context_id, procedure_id)
        dataset = self.find_create_dataset(request_body)

        model_info = Dataset.__get_model__(dataset['models'], request_body['id'])
        sample = Dataset.__prepare_sample__(model_info, request_body['tasks'])
        
        prediction = predict_entry(model=model, sample_input=sample)
        return prediction[0], accuracy
    
    def __create_dataset__(self, request_body: dict) -> Dataset:
        """ Create a new Dataset including one sample collection (ModelInfo) """

        dataset = Dataset(request = request_body)
        self._tenant_db.datasets.insert_one(json.loads(dataset.toJSON()))
        return dataset

    def __add_sample_collection__(self, 
        collection: str, 
        sample: [], 
        resolution: str,
        model_info: dict
    ):
        """ Add new sample to DB """
        
        sample_input = {}
        for idx, feature in enumerate(model_info['dataset_features']):
            sample_input[feature] = sample[idx]

        sample_collection = self._tenant_db[collection].insert_one({
            **sample_input,
            'resolution': resolution
        })

    def __save_model_to_db__(self, dataset: dict, model_info: dict, model, accuracy):
        """ Save binary model to DB """

        pickled_model = pickle.dumps(model)
        key = {
            'context_id': dataset['context_id'],
            'procedure_id': model_info['procedure_id'],
        }

        self._tenant_db.models.replace_one({**key}, {
            **key,
            'model': pickled_model,
            'accuracy': accuracy,
            'created_at': time.time()
        }, upsert=True)

    def __load_saved_model_from_db__(self, context_id: str, procedure_id: str):
        """ Load binary model based on Context and Procedure """

        model = self._tenant_db.models.find_one({
            'context_id': context_id,
            'procedure_id': procedure_id
        })
        
        return pickle.loads(model['model']), model['accuracy']