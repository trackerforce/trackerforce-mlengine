from utils import generate_id

class ModelInfo():
    def __init__(self, request: dict):
        self.procedure_id = request['id']
        self.collection_name = f'samples_{generate_id()}'
        self.dataset_features: list[str] = ModelInfo.__read_features__(request)

    @staticmethod
    def __read_features__(request: dict):
        features = []

        tasks = request['tasks']
        for task in tasks:
            task_id = task['id']
            task_learn = task['learn']

            if task_learn:
                ModelInfo.__read_options__(features, task_id, task)

        return features

    @staticmethod
    def __read_options__(features: list[str], task_id: str, task: dict):
        task_options = task.get('options', None)
        if task_options is None:
            features.append(f'{task_id}:value')
        else:
            for opt in task_options:
                features.append(f'{task_id}:{opt["value"]}')