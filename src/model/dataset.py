import json

from model.model import Model

class Dataset():
    def __init__(self, request: dict):
        self.context_id = request['contextId']
        self.models = [Model(request)]

    def toJSON(self):
        return json.dumps(self, default = lambda o: o.__dict__, 
            sort_keys = True, indent = 4)

    @staticmethod
    def __get_model__(models, procedure_id: str):
        for model in models:
            if model['procedure_id'] == procedure_id:
                return model

    @staticmethod
    def __prepare_sample__(model: dict, tasks: [dict]) -> []:
        data = []

        features = model['dataset_features']
        for feature in features:
            for task in tasks:
                task_id = task['id']
                task_learn = task['learn']

                if not task_learn:
                    continue

                feature_id = feature[0:feature.find(':')]
                feature_data = feature[feature.find(':')+1:len(feature)]
                if feature_id == task_id:
                    if feature_data != 'value':
                        data.append(1) if feature_data == task['response'] else data.append(0)
                    else:
                        data.append(float(task['response']))

        return data