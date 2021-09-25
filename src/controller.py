import json
from bson import json_util
from flask.wrappers import Request

import services.mongodb as db

def on_train(tenant: str, request: Request):
    tenant_db = db.get_tenant(tenant)

    # TODO: Create DatasetManager
    # - Validate if dataset exists / return it
    #   - Create dataset 
    # - Insert example
    # - Train model
    # - Update model
    return request.get_json()

def on_predict(tenant: str, request: Request):
    tenant_db = db.get_tenant(tenant)
    return request.get_json()