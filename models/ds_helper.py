from datetime import datetime
from google.cloud import datastore, storage
import re

pt_bucket = "rrcm-pt"

def check_duplicate(client, kind, param, val):
    query = client.query(kind=kind)
    query.add_filter(param, '=', val)
    return next(query.fetch(1), None)

def check_params(json_data, param_list):
    return all(param in json_data for param in param_list)

def get_next_id(client, counter_kind):
    key = client.key(counter_kind, 'id_counter')
    counter = client.get(key)
    if not counter:
        counter = datastore.Entity(key=key)
        counter['last_id'] = 0
    counter['last_id'] += 1
    client.put(counter)
    return counter['last_id']

def get_next_id2(client, counter_kind, parent):
    key = client.key(counter_kind, 'id_counter', parent=parent)
    counter = client.get(key)
    if not counter:
        counter = datastore.Entity(key=key)
        counter['last_id'] = 0
    counter['last_id'] += 1
    client.put(counter)
    return counter['last_id']

def create_entity(client, kind, cnt_kind, data, unique_list=[]):
    """ Create an entity using a complete key (kind and id).
        The id is generated for a specific counter kind.
        Put these operations in a transaction to prevent race conditions
    """
    with client.transaction():
        for param in unique_list:
            if check_duplicate(client, kind, param, data[param]):
                raise ValueError(param)
        
        entity_id = get_next_id(client, cnt_kind)
        key = client.key(kind, entity_id)
        entity = client.get(key)

        # Duplicated entity id
        if entity: raise ValueError("Entity ID")
        entity = datastore.Entity(key=key)
        entity.update(data)
        client.put(entity)

def create_entity_eval(client, kind, data):
    """ Create an entity using a complete key (kind and id).
        Put these operations in a transaction to prevent race conditions
    """ 
    key = client.key(kind, data["id"])
    entity = client.get(key)

    # Duplicated entity id
    if entity: raise ValueError("Entity ID")
    entity = datastore.Entity(key=key)
    entity.update(data)
    client.put(entity)

def update_entity(client, kind, id, data, unique_list=[]):
    """ Get an entity by a complete key (kind and id) to update its data.
        Ensure all values are not duplicated for params in the unique_list
    """
    key = client.key(kind, id)
    entity = client.get(key)

    if not entity:
        raise ValueError("Entity ID")

    for param in unique_list:
        # If param value is equal, no need to check for duplication
        if entity[param] == data[param]:
            continue

        if check_duplicate(client, kind, param, data[param]):
            raise ValueError(param)
    
    for key in data:
        entity[key] = data[key]
    
    client.put(entity)

def create_entity2(client, kind, cnt_kind, data, parent):
    entity_id = get_next_id2(client, cnt_kind, parent)
    key = client.key(kind, entity_id, parent=parent)
    entity = client.get(key)

    # Duplicated entity id
    if entity: raise ValueError("Entity ID")
    entity = datastore.Entity(key=key)
    entity.update(data)
    client.put(entity)
    
    return entity

def get_entity(client, kind, entity_id, parent=None):
    key = None
    if parent:
        key = client.key(kind, entity_id, parent=parent)
    else:
        key = client.key(kind, entity_id)

    return client.get(key)

def get_mime_type(base64_str):
    # Search for the pattern in the base64 string
    match = re.match(r'data:(.*?);base64,', base64_str)
    
    # Extract and return the MIME type if found
    if match:
        mime_type = match.group(1)
        return mime_type
    else:
        return None

def get_pt_folder(pt_hn):
    arr = pt_hn.split('-')
    n = int(arr[2])
    return f"site_{arr[0]}/{arr[1]}/{n // 1000 + 1}/f{n}"

def get_file_infos(bucket_name, prefix, f_dict):
    """ Get file infos conforming to f_dict:
    f_dict: {
      "pdgs": ["pdgl", "pdgr"],
      "models": ["model", "o1", "o2"],
    }
    """  
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    data_dict = {}
    for key in f_dict:
        if not key in data_dict: data_dict[key] = []
        for file_id in f_dict[key]:
            file_info = {"id": file_id, "info": None}
            blobs = bucket.list_blobs(prefix=prefix) # Need to list blobs every time since it is an iterator
            for blob in blobs:
                file_name = blob.name[len(prefix):]
                if file_name.startswith(file_info["id"]):
                    file_info["info"] = {
                        "prefix": prefix,
                        "file_name": file_name,
                        "mime_type": blob.content_type,
                        "file_size": blob.size
                    }
                    break # Go to next blob

            data_dict[key].append(file_info)

    return data_dict

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_entity_count(client, kind, filters=[]):
    # Create a query object with keys only
    query = client.query(kind=kind)
    for f in filters:
        query.add_filter(f["param"], f["operator"], f["value"])
    query.keys_only()
    
    total_entities = 0
    query_iter = query.fetch()
    
    # Use cursors to handle large datasets
    while True:
        batch = list(query_iter)
        total_entities += len(batch)
        if query_iter.next_page_token:
            query_iter = query.fetch(start_cursor=query_iter.next_page_token)
        else:
            break
    
    return total_entities

def paginate(client, kind, start_index, page_size, filters=[], order=None):
    page_number = (start_index // page_size) + 1

    # Create a query object
    query = client.query(kind=kind)

    for f in filters:
        query.add_filter(f["param"], f["operator"], f["value"])
        
    if order:
        if order["asc"]:
            query.order = [order["param"]]
        else:
            query.order = [f"-{order['param']}"]

    query.keys_only()
    
    query_iter = query.fetch(limit=page_size)
    last_cursor = None

    # Skip to the desired page by iterating through keys only
    for _ in range(page_number - 1):
        for _ in query_iter:
            pass  # Iterate through the entities just to advance the cursor
        if query_iter.next_page_token:
            last_cursor = query_iter.next_page_token
            query_iter = query.fetch(start_cursor=query_iter.next_page_token, limit=page_size)
        else:
            return []
            
    # Fetch the full data for the desired page
    query = client.query(kind=kind)

    for f in filters:
        query.add_filter(f["param"], f["operator"], f["value"])
        
    if order:
        if order["asc"]:
            query.order = [order["param"]]
        else:
            query.order = [f"-{order['param']}"]

    if last_cursor:
        query_iter = query.fetch(start_cursor=last_cursor, limit=page_size)
    else:
        query_iter = query.fetch(limit=page_size)

    return list(query_iter)