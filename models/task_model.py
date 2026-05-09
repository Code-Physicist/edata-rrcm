import re
from google.cloud import datastore
from datetime import datetime
from models import ds_helper

kind = "Task"
def create(json_data):
    data = {}
    data['job_id'] = int(json_data["job_id"])
    data['opn_id'] = int(json_data["opn_id"])
    data["site_id"] = int(json_data["site_id"])
    data["user_id"] = 0
    data["start_time"] = None
    data["end_time"] = None

    client = datastore.Client()
    with client.transaction():
        # Todo: check duplicated task based on job_id & opn_id
        entity = datastore.Entity(key=client.key(kind))
        entity.update(data)
        client.put(entity)

    #job_id, opn_id, [task_data], site_id, user_id, start_time, end_time

        