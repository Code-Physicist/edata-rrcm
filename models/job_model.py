import re
from google.cloud import datastore
from datetime import datetime
from models import ds_helper

kind = "Job"
cnt_kind = "JobCounter"

def create(json_data, site_id):
    data = {}
    data['lot_id'] = json_data["lot_id"]
    data['pt_hn'] = json_data["pt_hn"]
    data['type_id'] = 1 # 1 => step, 2 => produce
    data['route_id'] = int(json_data["route_id"])
    data['priority'] = int(json_data["priority"])
    data['opn_id'] = "" # Start with empty string
    data["site_id"] = site_id
    data["p_site_id"] = site_id # Original site
    data["cross"] = 0 # 0 => in-site job, 1 => cross-site job
    data["user_id"] = 0
    data["number"] = int(json_data["number"])
    data["status"] = 0

    client = datastore.Client()
    with client.transaction():
        query = client.query(kind=kind)
        query.add_filter("lot_id", '=', data['lot_id']).add_filter("pt_hn", '=', data['pt_hn'])
        if next(query.fetch(1), None):
            raise ValueError("pt_hn")

        entity_id = ds_helper.get_next_id(client, cnt_kind)
        key = client.key(kind, entity_id)
        entity = client.get(key)

        # Duplicated entity id
        if entity: raise ValueError("Entity ID")
        entity = datastore.Entity(key=key)
        entity.update(data)
        client.put(entity)

def get(lot_id, site_id):
    client = datastore.Client()
    data_list = list(client.query(kind=kind).add_filter("lot_id", "=", lot_id).fetch())
    for data in data_list:
        data["id"] = int(data.key.id_or_name)
        pt = next(client.query(kind=f"Patient_{site_id}").add_filter("hn", "=", data["pt_hn"]).fetch(1), None)
        data["pt_name"] = ' '.join([s for s in [pt["prefix"], pt["first_name"], pt["middle_name"], pt["last_name"]] if s])
    return data_list

def delete(job_id):
    client = datastore.Client()
    key = client.key(kind, job_id)
    client.delete(key)

        
        
        
