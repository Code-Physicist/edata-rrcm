import re
from datetime import datetime
from google.cloud import datastore
from models import ds_helper
import hashlib

kind = "User"
cnt_kind = "UserCounter"
param_list = ["id", "username", "id_card", "prefix", "first_name", "last_name", "phone", "address", "site_id", "roles"]
unique_list = ["username", "id_card"]

def create(json_data):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]

    password = "admin1234" 
    data["password"] = hashlib.md5(password.encode('UTF-8')).hexdigest()
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
    
    id = int(json_data["id"])
    
    client = datastore.Client()
    ds_helper.update_entity(client, kind, id, data, unique_list)

def get():
    client = datastore.Client()
    users = list(client.query(kind=kind).fetch())
    for user in users:
        user["id"] = user.key.id_or_name
    return users



