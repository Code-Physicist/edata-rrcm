from datetime import datetime
from google.cloud import datastore
from models import ds_helper

kind = "Route"
cnt_kind = "RouteCounter"
param_list = ["id", "code", "name", "description", "operations", "is_active"]
unique_list = ["code"]

def create(json_data):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")

    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]

    opns = []
    opn_ids = []
    operations = data["operations"]
    for opn in operations:
        opns.append({"order": opn["order"], "id": opn["id"]})
        opn_ids.append(opn["id"])
    
    data["operations"] = opns
    data["opn_ids"] = opn_ids
    data["is_active"] = True
    data['create_time'] = datetime.utcnow()

    client = datastore.Client()
    with client.transaction():
        for param in unique_list:
            if ds_helper.check_duplicate(client, kind, param, data[param]):
                raise ValueError(param)
            
        data["id"] = ds_helper.get_next_id(client, cnt_kind)
        ds_helper.create_entity_eval(client, kind, data)

def update(json_data):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]
    
    opns = []
    opn_ids = []
    operations = data["operations"]
    for opn in operations:
        opns.append({"order": opn["order"], "id": opn["id"]})
        opn_ids.append(opn["id"])
    
    data["operations"] = opns
    data["opn_ids"] = opn_ids
    
    id = int(json_data["id"])
    
    client = datastore.Client()
    ds_helper.update_entity(client, kind, id, data, unique_list)

def get():
    client = datastore.Client()
    routes = list(client.query(kind=kind).fetch())
    for route in routes:
        route["id"] = route.key.id_or_name
    
    return routes