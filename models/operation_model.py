from datetime import datetime
from google.cloud import datastore
from models import ds_helper

kind = "Operation"
param_list = ["id", "name", "description", "type"]

def create(json_data):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    data = {}
    for param in param_list:
        data[param] = json_data[param]
    
    # Make sure type is integer
    data["type"] = int(data["type"])
    data['create_time'] = datetime.utcnow()

    client = datastore.Client()
    with client.transaction():
        ds_helper.create_entity_eval(client, kind, data)

def update(json_data):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    id = json_data["id"]

    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]
    
    # Make sure type is integer
    data["type"] = int(data["type"])

    client = datastore.Client()
    ds_helper.update_entity(client, kind, id, data)

def get():
    client = datastore.Client()
    return list(client.query(kind=kind).fetch())