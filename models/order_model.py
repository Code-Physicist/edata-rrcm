import re
from google.cloud import datastore
from datetime import datetime, timedelta
from models import ds_helper, job_model
from zoneinfo import ZoneInfo

kind = "Order"
cnt_kind = "OrderCounter"
param_list = ["id", "lot_id", "site_id", "route_id", "priority", "create_time"]
unique_list = ['lot_id']

def create(json_data, site_id):
    data = {}
    data['lot_id'] = json_data["lot_id"]
    data["site_id"] = site_id
    data["route_id"] = int(json_data["route_id"])
    data["priority"] = int(json_data["priority"])
    data["status"] = 0 # 0 => Draft, 1 => Open, 2 => Closed
    data['create_time'] = datetime.utcnow()
    data['submit_time'] = None

    key = None
    client = datastore.Client()
    with client.transaction():
        for param in unique_list:
            if ds_helper.check_duplicate(client, kind, param, data[param]):
                raise ValueError(param)
                    
        site_id, site_code, today, num = get_next_lot_info(client, site_id)
        if data["lot_id"] != f"{site_code}-{today}-{str(num).zfill(3)}":
            raise ValueError("lot_id")
        
        counter_key = client.key("LotCounter", site_code)
        counter = client.get(counter_key)
        if not counter:
            counter = datastore.Entity(key=counter_key)
            counter.update({"date": today, "number": num})
        else:
            counter["date"] = today
            counter["number"] = num
        client.put(counter)
        
        data["id"] = int(f"{site_id}{today}{num}")
        ds_helper.create_entity_eval(client, kind, data)

    # Getting order after put using key lookup to avoid eventual consistency 
    order = client.get(client.key(kind, data["id"]))
    return order

def submit(order_id):
    client = datastore.Client()
    with client.transaction():
        order = client.get(client.key("Order", order_id))
        if not order:
            raise ValueError("id")

        if order["status"] != 0:
            raise ValueError("status")
        
        submit_time = datetime.utcnow()
        target_time = submit_time + timedelta(days=6)

        order["status"] = 1
        order["submit_time"] = submit_time
        client.put(order)

        route = ds_helper.get_entity(client, "Route", order["route_id"])
        if not route:
            raise ValueError("route_id")
        
        opns = sorted(route["operations"], key=lambda x: x['order'])

        jobs = list(client.query(kind="Job").add_filter("lot_id", "=", order["lot_id"]).fetch())
        for job in jobs:
            job["opn_id"] = opns[0]['id']
            job["target_time"] = target_time
            job["status"] = 0
            client.put(job)
        
        if jobs:
            client.put_multi(jobs)


def get(status, site_id):
    client = datastore.Client()
    query1 = client.query(kind=kind).add_filter("site_id", "=", site_id).add_filter("status", "=", status)
    list1 = list(query1.fetch())
    #query2 = client.query(kind=kind).add_filter("site_id", "=", site_id).add_filter("status", "=", 1)
    #list2 = list(query2.fetch())

    # Find common entities based on matching keys
    #list1_keys = {entity.key: entity for entity in list1}

    #for entity in list2:
    #    if not entity.key in list1_keys:
    #        list1.append(entity)
    
    for data in list1:
        data["id"] = int(data.key.id_or_name)
    
    # Construct route dictionary and let JS use it
    routes = list(client.query(kind="Route").fetch())
    route_dict = {}
    for route in routes:
        route_dict[int(route.key.id_or_name)] = f"{route['code']} {route['name']}"
        
    return list(list1), route_dict

def get_next_lot(site_id):
    client = datastore.Client()
    site_id, site_code, today, num = get_next_lot_info(client, site_id)
    return f"{site_code}-{today}-{str(num).zfill(3)}"

def get_next_lot_info(client, site_id):
    site_key = client.key("Site", site_id)
    site = client.get(site_key)

    now = datetime.now(ZoneInfo("Asia/Bangkok"))
    year = now.year % 100
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    today = f"{year}{month}{day}"

    # Ex. site.code = 99 (Footcare), KP (Khokpho)
    counter_key = client.key("LotCounter", site["code"])
    counter = client.get(counter_key)
    
    if not counter or today != counter["date"]:
        return int(site["id"]), site["code"], today, 1
    
    num = counter["number"] + 1
    return int(site["id"]), site["code"], today, num




    

        
        
