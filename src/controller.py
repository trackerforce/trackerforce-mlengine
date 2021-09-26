import json
from bson import json_util

import services.mongodb as db
from services.dataset_manager import DatasetManager

def on_train(tenant: str, request_body: dict):
    context_id = request_body['contextId']
    tenant_db = db.get_tenant(tenant)

    # TODO: Create DatasetManager
    # - Insert example
    # - Train model
    # - Update model

    dsm = DatasetManager(tenant_db)
    ds = dsm.find_create_dataset(request_body)
    dsm.insert_example(ds, request_body)

    # dsm.train(request_body)
    return ds

def on_predict(tenant: str, request_body: dict):
    tenant_db = db.get_tenant(tenant)
    return request_body