import os
from google.cloud import datastore, storage
from datetime import datetime
from models import ds_helper
import base64

kind = "MedJob"
param_list = ["id", "pt_hn", "opn_id", "user_id", "status", "start_time", "end_time"]
bucket_name = "rrcm-med-job"

def create(client, json_data, site_id):
    data = {}
    data['pt_hn'] = json_data["pt_hn"]
    data["opn_id"] = json_data["opn_id"]
    data["user_id"] = json_data["user_id"]
    data["start_time"] = datetime.utcnow()

    init_opn_data(data["opn_id"], data)

    site_key = client.key('Site', int(site_id))

    # Since med_job and appt are 1:1, let use the same id
    key = client.key(kind, int(json_data["appt_id"]), parent=site_key)
    med_job = client.get(key)
    if med_job: raise ValueError("Entity ID")

    med_job = datastore.Entity(key=key)
    med_job.update(data)
    client.put(med_job)

def init_opn_data(opn_id, data):
    if opn_id == "D02":
        data["pdgl"] = "" 
        data["pdgr"] = ""
        data["model"] = "" 
        data["o1"] = ""
        data["o2"] = ""

        data["smg"] = 0
        data["mpd"] = ""
        data["bsl"] = ""
        data["fw"] = 0
        data["cut"] = 0
        data["cutd"] = ""
        data["numb"] = 0
        data["symp1"] = True
        data["symp2"] = False
        data["symp3"] = False
        data["shoe"] = ""
        data["fit"] = 1
        data["sock"] = 1
        data["foot_l"] = [
            { "data": [True, False, False, False] },
            { "data": [True, False, False, False, False, False] },
            { "data": [True, False, False, False] },
            { "data": 1 },
            { "data": 1 },
            { "data": [True, False, False] },
            { "data": 1 },
            { "data": 1 },
        ]
        data["foot_r"] = [
            { "data": [True, False, False, False] },
            { "data": [True, False, False, False, False, False] },
            { "data": [True, False, False, False] },
            { "data": 1 },
            { "data": 1 },
            { "data": [True, False, False] },
            { "data": 1 },
            { "data": 1 },
        ]
        data["wound"] = 0
        data["wsd"] = ""
        data["gan"] = 0
        data["wrn"] = ""
        data["risk"] = 1
        data["r_check"] = [False,False,False,False,False,False,False,False,False,False]
        data["o_cure"] = ""
        data["phys_id"] = 0
        data["next_opd"] = ""
        data["f2_state"] = "33333333"
    else:
        raise Exception("Invalid Operation")

def upload_file(mj_id, pt_hn, file_id, file):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(ds_helper.pt_bucket)

    ext = os.path.splitext(file.filename)[1] # Ex: .png, .jpg
    pt_folder = ds_helper.get_pt_folder(pt_hn)
    prefix = f"{pt_folder}/med_job_{mj_id}/"
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        if blob.name[len(prefix):].startswith(file_id):
            blob.delete()
    
    file_name = f"{file_id}{ext}"
    blob = bucket.blob(f"{prefix}{file_name}")
    blob.upload_from_file(file, content_type=file.content_type)

    return {"prefix": prefix, "file_name": file_name, "mime_type": file.content_type, "file_size": blob.size}

def download_file(file_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(ds_helper.pt_bucket)

    blob = bucket.blob(file_path)

    if blob.exists():
        return blob.download_as_bytes(), blob.content_type
    else:
        return None, None

def get_file(pt_hn, mj_id, file_name):
    pt_folder = ds_helper.get_pt_folder(pt_hn)
    file_path = f"{pt_folder}/med_job_{mj_id}/{file_name}"
    return download_file(file_path)

def submit(json_data, site_id):
    data = json_data["med_job"]
    
    client = datastore.Client()

    with client.transaction():
        id = int(data["id"])
        appt = ds_helper.get_entity(client, "Appointment", id, client.key('Site', int(site_id)))
        if not appt:
            raise ValueError("Invalid Appointment")

        if appt["status"] == 0:
            raise ValueError("Invalid Status")
        
        if appt["status"] == 1:
            appt["status"] = 2 # 1 => Working, 2 => Done
            client.put(appt)

        med_job = ds_helper.get_entity(client, kind, id, client.key('Site', int(site_id)))
        if not med_job:
            raise ValueError("Invalid Med Job")
        
        for param in data:
            if param == "id" or param == "pt_hn": continue
            med_job[param] = data[param]

        med_job["end_date_time"] = datetime.utcnow()   
        client.put(med_job)

        if data["opn_id"] == "D02":
            f4_overlay = json_data["f4_overlay"]
            if f4_overlay != "":
                storage_client = storage.Client()
                bucket = storage_client.bucket(ds_helper.pt_bucket)
                pt_folder = ds_helper.get_pt_folder(med_job["pt_hn"])
                prefix = f"{pt_folder}/med_job_{med_job.key.id_or_name}/"
                image_data = base64.b64decode(f4_overlay.split(",")[1])
                blob = bucket.blob(f"{prefix}f4.png")
                blob.upload_from_string(image_data, content_type=ds_helper.get_mime_type(f4_overlay))



        
        
