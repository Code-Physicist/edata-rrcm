import re
from google.cloud import datastore, storage
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from models import ds_helper
import base64

#site id = 1, Kind = "Patient_1"
kind = "Patient"

#HN and id are the same
param_list = [
    "hn", "photo", "id_card", "passport", "prefix", "first_name", "middle_name", "last_name", "gender",
    "birth_date", "blood_type", "nationality_id", "nationality", "race", "right_id", "right", "drug_allergy", "cong_disease", 
    "address", "phone", "mobile", "email", "line_id"
]
unique_list = ["id_card", "passport"]

def create(json_data, site_id):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    data = {}
    for param in param_list:
        if param == "hn" or param == "photo": continue
        data[param] = json_data[param]
    data["create_time"] = datetime.utcnow()

    client = datastore.Client()
    with client.transaction():
        for param in unique_list:
            # Empty value is allowed
            if data[param] == "":
                continue

            if ds_helper.check_duplicate(client, f"{kind}_{site_id}", param, data[param]):
                raise ValueError(param)
                
        site_code, year, num_str = get_next_hn(client, site_id)
        data["hn"] = f"{site_code}-{year}-{num_str}"
        num_int = int(num_str)
        id = int(f"{site_id}{year}{num_int}")
        
        entity = datastore.Entity(key=client.key(f"{kind}_{site_id}", id))
        entity.update(data)
        client.put(entity)

        # Base64 string
        photo = json_data["photo"]
        if photo != "":
            mime_type = ds_helper.get_mime_type(photo)
            if not mime_type or (mime_type != "image/jpeg" and mime_type != "image/png"):
                raise ValueError("photo")

            ext = ".png" if mime_type == "image/png" else ".jpg"
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(ds_helper.pt_bucket)
            image_data = base64.b64decode(photo.split(",")[1])
        
            # Create a new blob and upload the image data
            pt_folder = ds_helper.get_pt_folder(data['hn'])
            blob = bucket.blob(f"{pt_folder}/photo/photo{ext}")
            blob.upload_from_string(image_data, content_type=mime_type)

def update(json_data, site_id):
    if not ds_helper.check_params(json_data, param_list):
        raise Exception("Bad request")
    
    client = datastore.Client()
    entity = next(client.query(kind=f"{kind}_{site_id}").add_filter("hn", "=", json_data["hn"]).fetch(1), None)
    if not entity:
        raise ValueError("hn")
    
    for param in unique_list:
        # If the value is empty or equal to the old value, allow it
        if json_data[param] == "" or entity[param] == json_data[param]:
            continue

        if ds_helper.check_duplicate(client, f"{kind}_{site_id}", param, json_data[param]):
            raise ValueError(param)
        
    for param in json_data:
        # HN won't be updated. Photo will be updated in other request
        if param == "hn" or param == "photo": continue
        entity[param] = json_data[param]
    
    client.put(entity)

    photo = json_data["photo"]
    if photo != "":
        mime_type = ds_helper.get_mime_type(photo)
        if not mime_type or (mime_type != "image/jpeg" and mime_type != "image/png"):
            raise ValueError("photo")

        ext = ".png" if mime_type == "image/png" else ".jpg"
        image_data = base64.b64decode(photo.split(",")[1])

        storage_client = storage.Client()
        bucket = storage_client.bucket(ds_helper.pt_bucket)
        pt_folder = ds_helper.get_pt_folder(json_data['hn'])
        prefix = f"{pt_folder}/photo/"
        
        blobs = bucket.list_blobs(prefix=prefix)
        for blob in blobs:
            if blob.name[len(prefix):].startswith("photo"):
                blob.delete()

        blob = bucket.blob(f"{prefix}photo{ext}")
        blob.upload_from_string(image_data, content_type=mime_type)

def get(site_id):
    client = datastore.Client()
    query = client.query(kind=f"{kind}_{site_id}")   
    query.order = ['-create_time']

    # Fetch latest 100 patients
    return list(query.fetch(100))

def get_photo(hn):
    pt_folder = ds_helper.get_pt_folder(hn)
    storage_client = storage.Client()
    bucket = storage_client.bucket(ds_helper.pt_bucket)
    prefix = f"{pt_folder}/photo/"

    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        if blob.name[len(prefix):].startswith("photo"):
            return blob.download_as_bytes(), blob.content_type
        
    raise ValueError("photo")

def search(search_param, search_prefix, site_id):
    if search_param == "full_name":
        return search_full_name(search_prefix, site_id)
    
    client = datastore.Client()
    query = client.query(kind=f"{kind}_{site_id}")
    query.add_filter(search_param, '>=', search_prefix)
    query.add_filter(search_param, '<=', search_prefix + "\ufffd")
    return list(query.fetch())

def search_full_name(prefix, site_id):
    client = datastore.Client()
    # Create queries with the prefix range for both properties
    end_range = prefix + "\ufffd"

    # Perform the range query for first name
    first_name_query = client.query(kind=f"{kind}_{site_id}")
    first_name_query.add_filter("first_name", '>=', prefix)
    first_name_query.add_filter("first_name", '<=', end_range)
    first_name_results = list(first_name_query.fetch())

    # Perform the range query for middle name
    middle_name_query = client.query(kind=f"{kind}_{site_id}")
    middle_name_query.add_filter("middle_name", '>=', prefix)
    middle_name_query.add_filter("middle_name", '<=', end_range)
    middle_name_results = list(middle_name_query.fetch())

    # Perform the range query for last name
    last_name_query = client.query(kind=f"{kind}_{site_id}")
    last_name_query.add_filter("last_name", '>=', prefix)
    last_name_query.add_filter("last_name", '<=', end_range)
    last_name_results = list(last_name_query.fetch())

    # Find common entities based on matching keys
    first_name_keys = {entity.key: entity for entity in first_name_results}

    for entity in middle_name_results:
        if not entity.key in first_name_keys:
            first_name_results.append(entity)

    for entity in last_name_results:
        if not entity.key in first_name_keys:
            first_name_results.append(entity)

    return first_name_results

def get_next_hn(client, site_id):
    key = client.key("Site", site_id)
    site = client.get(key)

    tz = ZoneInfo("Asia/Bangkok")
    year = datetime.now(tz).year % 100 # Get the last 2 digits. Ex. 2024 => 24

    # Ex. site.code = 99 (Footcare), KP (Khokpho)
    key = client.key("HNCounter", site["code"])
    counter = client.get(key)
    
    if not counter:
        counter = datastore.Entity(key=key)
        counter['last_id'] = f"{year}-000000"
    
    parts = counter["last_id"].split("-")
    if year == int(parts[0]):
        parts[1] = str(int(parts[1]) + 1).zfill(6)
    else:
        parts[1] = "000001"
    
    counter["last_id"] = f"{year}-{parts[1]}"
    client.put(counter)
    
    #return f"{site["code"]}-{counter['last_id']}"
    return site["code"], year, parts[1]