import json
from bson import json_util

import services.mongodb as db
from services.dataset_manager import DatasetManager

def on_train(tenant: str, request_body: dict):
    context_id = request_body['contextId']
    tenant_db = db.get_tenant(tenant)

    # Initialize DatasetManager
    dsm = DatasetManager(tenant_db)

    # Retrieve or create Dataset
    ds = dsm.find_create_dataset(request_body)

    # Populate sample and return the Dataset model info
    mi = dsm.insert_example(ds, request_body)

    # Train and update Dataset model
    accuracy = dsm.train_update(dataset=ds, model_info=mi)
    
    return {
        **ds,
        'accuracy': accuracy * 100
    }

def on_predict(tenant: str, request_body: dict):
    tenant_db = db.get_tenant(tenant)
    return request_body