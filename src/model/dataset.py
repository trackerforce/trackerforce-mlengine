import json

from model.model_info import ModelInfo

class Dataset():
    def __init__(self, request: dict):
        self.context_id = request['context_id']
        self.models = [ModelInfo(request)]

    def to_json(self):
        return json.dumps(self, default = lambda o: o.__dict__, 
            sort_keys = True, indent = 4)

    @staticmethod
    def __get_model__(models, procedure_id: str):
        for model in models:
            if model['procedure_id'] == procedure_id:
                return model

    @staticmethod
    def __prepare_sample__(model: dict, tasks: list[dict]) -> list:
        data = []

        features = model['dataset_features']
        for feature in features:
            Dataset.process_task_feature(tasks, data, feature)

        return data

    @staticmethod
    def process_task_feature(tasks, data, feature):
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
                    data.append(task['response'])