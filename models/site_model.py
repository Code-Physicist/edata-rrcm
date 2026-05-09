from datetime import datetime
from google.cloud import datastore
from models import ds_helper

kind = "Site"
cnt_kind = "SiteCounter"
param_list = ["id", "code", "name", "address", "province_id", "amphur_id", "tambon_id", "latitude", "longitude", "operations"]
unique_list = ["code", "name"]

def create(json_data):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]
        
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
    
    id = int(json_data["id"])

    data = {}
    for param in param_list:
        if param == "id": continue
        data[param] = json_data[param]
    
    client = datastore.Client()
    ds_helper.update_entity(client, kind, id, data, unique_list)

def get():
    client = datastore.Client()
    sites = list(client.query(kind=kind).fetch())
    for site in sites:
        site["id"] = site.key.id_or_name
        p = list(client.query(kind="Province").add_filter("id", "=", site["province_id"]).fetch(1))
        a = list(client.query(kind="Amphur").add_filter("id", "=", site["amphur_id"]).fetch(1))
        t = list(client.query(kind="Tambon").add_filter("id", "=", site["tambon_id"]).fetch(1))
        site["province"] = p[0]["name_th"]
        site["amphur"] = a[0]["name_th"]
        site["tambon"] = t[0]["name_th"]
        site["zip_code"] = t[0]["zip_code"]
    
    return sites
