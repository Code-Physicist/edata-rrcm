from google.cloud import datastore
from models import ds_helper

#site id = 1, Kind = "Patient_1", cnt_kind = "PhysCounter_1"
kind = "Physician"
cnt_kind = "PhysCounter"

#HN id and id are the same
param_list = ["id", "prefix", "first_name", "last_name"]

def create(json_data, site_id):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]

    client = datastore.Client()
    with client.transaction():    
        data["id"] = ds_helper.get_next_id(client, f"{cnt_kind}_{site_id}")
        ds_helper.create_entity_eval(client, f"{kind}_{site_id}", data)

def update(json_data, site_id):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    entity_id = int(json_data["id"])

    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]
    
    client = datastore.Client()
    ds_helper.update_entity(client, f"{kind}_{site_id}", entity_id, data)

def get(site_id):
    client = datastore.Client()
    data_list = list(client.query(kind=f"{kind}_{site_id}").fetch())
    for data in data_list:
        data["id"] = int(data.key.id_or_name)
    return data_list