from google.cloud import datastore, storage
from datetime import datetime
from models import ds_helper, med_job_model

kind = "Appointment"
cnt_kind = "ApptCounter"
param_list = ["id", "pt_hn", "opn_id", "user_id", "appt_time", "note", "status"]

def create(json_data, site_id):
    data = {}
    data['pt_hn'] = json_data["pt_hn"]
    data["opn_id"] = json_data["opn_id"]
    data["user_id"] = int(json_data["user_id"])
    data["note"] = json_data["note"]
    data["status"] = 0 # 0 => Idle, 1 => Working, 2 => Done
    data["appt_time"] = datetime.strptime(json_data["appt_time"],'%Y-%m-%dT%H:%M:%SZ')

    client = datastore.Client()
    with client.transaction():
        # Check if the patient exists
        query = client.query(kind=f"Patient_{site_id}")
        query.add_filter("hn", "=", data["pt_hn"])
        patient = next(query.fetch(1), None)
        if not patient:
            raise Exception("Patient")
    
        # Overwrite patient mobile
        if "pt_mobile" in json_data and patient["mobile"] != json_data["pt_mobile"]:
            patient["mobile"] = json_data["pt_mobile"]
            client.put(patient)

        ds_helper.create_entity2(client, kind, cnt_kind, data, client.key('Site', site_id))

def get(json_data, site_id, user_id = None):
    start_dt = datetime.strptime(json_data["start_date_time"],'%Y-%m-%dT%H:%M:%SZ')
    end_dt = datetime.strptime(json_data["end_date_time"],'%Y-%m-%dT%H:%M:%SZ')
    client = datastore.Client()
    query = client.query(kind=kind, ancestor=client.key('Site', site_id))

    query.add_filter("appt_time", ">=", start_dt)
    query.add_filter("appt_time", '<=', end_dt)
    
    if user_id:
        query.add_filter("user_id", "=", int(user_id))

    appts = list(query.fetch())

    opn_dict = {}
    user_dict = {}
    for appt in appts:
        appt["id"] = int(appt.key.id_or_name)
        query = client.query(kind=f"Patient_{site_id}")
        query.add_filter("hn", "=", appt["pt_hn"])
        patient = next(query.fetch(1), None)
        if patient:
            appt["pt_name"] = ' '.join([s for s in [patient["prefix"], patient["first_name"], patient["middle_name"], patient["last_name"]] if s])
            appt["pt_mobile"] = patient["mobile"]
            appt["birth_date"] = patient["birth_date"]
        
        opn_id = appt["opn_id"]
        if opn_id in opn_dict:
            appt["opn_name"] = opn_dict[opn_id]
        else:
            opn = ds_helper.get_entity(client, "Operation", opn_id)
            if opn:
                opn_dict[opn_id] = opn["name"]
                appt["opn_name"] = opn["name"]
        
        user_id = appt["user_id"]
        if user_id in user_dict:
            appt["u_name"] = user_dict[user_id]
        else:
            user = ds_helper.get_entity(client, "User", user_id)
            if user:
                u_name = ' '.join([s for s in [user["prefix"], user["first_name"], user["last_name"]] if s])
                user_dict[user_id] = u_name
                appt["u_name"] = u_name

    return appts

def check_in(json_data, site_id, user_id):
    appt_id = int(json_data["appt_id"])

    client = datastore.Client()
    with client.transaction():
        site_key = client.key('Site', site_id)
        appt = ds_helper.get_entity(client, kind, appt_id, site_key)
        if not appt:
            raise ValueError("Invalid Appointment")

        if appt["user_id"] != user_id:
            raise ValueError("Invalid User")

        if appt["status"] == 0:
            appt["status"] = 1
            client.put(appt)

        med_job = ds_helper.get_entity(client, "MedJob", appt_id, site_key)
        if not med_job:
            data = {}
            data["pt_hn"] = appt["pt_hn"]
            data["user_id"] = appt["user_id"]
            data["opn_id"] = appt["opn_id"]
            data["appt_id"] = appt_id
            med_job_model.create(client, data, site_id)

    med_job = ds_helper.get_entity(client, "MedJob", appt_id, site_key)
    med_job["id"] = int(med_job.key.id_or_name)

    pt_folder = ds_helper.get_pt_folder(med_job["pt_hn"])
    file_infos = ds_helper.get_file_infos(ds_helper.pt_bucket, f"{pt_folder}/med_job_{med_job["id"]}/", json_data["f_dict"])
    return med_job, file_infos
