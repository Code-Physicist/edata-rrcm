import os
from flask import Blueprint, request, redirect, jsonify, make_response
from auth.auth import check_admin, check_roles, admin_response
from google.cloud import datastore

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))

    return admin_response('dashboard.html', user_data)

@dashboard_bp.route("/api/get_sites")
def get_sites():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Site").fetch())
    for data in data_list:
        data["id"] = int(data.key.id_or_name)

    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_operations")
def get_operations():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Operation").fetch())
    for data in data_list:
        data["id"] = int(data.key.id_or_name)

    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_routes")
def get_routes():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Route").fetch())
    for data in data_list:
        data["id"] = int(data.key.id_or_name)
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_users", methods=["POST"])
def get_operators():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    opn_id = request.json["opn_id"]
    client = datastore.Client()
    users = list(client.query(kind="User").add_filter("site_id", "=", user_data["site_id"]).fetch())
    data_list = []
    for user in users:
        roles = user["roles"]
        for role in roles:
            if role["opn_id"] == opn_id and (role["role_type"] == 1 or role["role_type"] == 3):
                data_list.append(user)

    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_users2", methods=["POST"])
def get_operators2():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    opn = client.get(client.key("Operation", request.json["opn_id"]))
    users = list(client.query(kind="User").add_filter("site_id", "=", user_data["site_id"]).fetch())
    data_list = []
    for user in users:
        roles = user["roles"]
        for role in roles:
            if role["opn_id"] == opn["id"] and (role["role_type"] == 1 or role["role_type"] == 3):
                user["id"] = user.key.id_or_name
                data_list.append(user)

    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_med_operations", methods=["POST"])
def get_med_operations():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Operation").add_filter("type", "=", 1).add_filter("id", "=", "D02").fetch())

    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_provinces")
def get_provinces():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Province").fetch())
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_amphurs")
def get_amphurs():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})
        
    client = datastore.Client()
    parent_id = int(request.args.get('province_id'))
    data_list = list(client.query(kind="Amphur").add_filter("province_id", "=", parent_id).fetch())
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_tambons")
def get_tambons():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    parent_id = int(request.args.get('amphur_id'))
    data_list = list(client.query(kind="Tambon").add_filter("amphur_id", "=", parent_id).fetch())
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_amphurs_tambons")
def get_amphurs_tambons():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    province_id = int(request.args.get('province_id'))
    amphur_id = int(request.args.get('amphur_id'))

    amphurs = list(client.query(kind="Amphur").add_filter("province_id", "=", province_id).fetch())
    tambons = list(client.query(kind="Tambon").add_filter("amphur_id", "=", amphur_id).fetch())
    return jsonify({"status":"T", "amphurs": amphurs, "tambons":tambons})

@dashboard_bp.route("/api/get_nationalities")
def get_nationalities():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Nationality").fetch())
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_prefixes")
def get_prefixes():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})

    client = datastore.Client()
    data_list = list(client.query(kind="Prefix").fetch())
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/api/get_rights")
def get_rights():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"})
        
    client = datastore.Client()
    data_list = list(client.query(kind="PtRight").fetch())
    return jsonify({"status":"T", "data_list": data_list})

@dashboard_bp.route("/upload/nationality", methods=["POST"])
def upload_country():
    if request.json["secret"] != os.environ.get('UPLOAD_SECRET'):
        return jsonify({"status": "error"}), 400

    ID = request.json["id"]
    name = request.json["name"]

    client = datastore.Client()
    entity = datastore.Entity(key=client.key("Nationality"))
    entity.update(
        {
            'id': ID,
            'name':name
        }
    )
    client.put(entity)

    return "ok"

@dashboard_bp.route("/upload/prefix", methods=["POST"])
def upload_prefix():
    if request.json["secret"] != os.environ.get('UPLOAD_SECRET'):
        return jsonify({"status": "error"}), 400

    ID = request.json["id"]
    prefix = request.json["prefix"]

    client = datastore.Client()
    entity = datastore.Entity(key=client.key("Prefix"))
    entity.update(
        {
            'id': ID,
            'prefix':prefix
        }
    )
    client.put(entity)

    return "ok"

@dashboard_bp.route("/upload/right", methods=["POST"])
def upload_benefit():
    if request.json["secret"] != os.environ.get('UPLOAD_SECRET'):
        return jsonify({"status": "error"}), 400

    ID = request.json["id"]
    right = request.json["right"]

    client = datastore.Client()
    entity = datastore.Entity(key=client.key("PtRight"))
    entity.update(
        {
            'id': ID,
            'name':right
        }
    )
    client.put(entity)

    return "ok"

@dashboard_bp.route("/upload/province", methods=["POST"])
def upload_province():
    if request.json["secret"] != os.environ.get('UPLOAD_SECRET'):
        return jsonify({"status": "error"}), 400

    ID = request.json["id"]
    name_th = request.json["name_th"]
    name_en = request.json["name_en"]

    client = datastore.Client()
    entity = datastore.Entity(key=client.key("Province"))
    entity.update(
        {
            'id': ID,
            'name_th':name_th,
            'name_en':name_en
        }
    )
    client.put(entity)

    return "ok"

@dashboard_bp.route("/upload/amphur", methods=["POST"])
def upload_amphur():
    if request.json["secret"] != os.environ.get('UPLOAD_SECRET'):
        return jsonify({"status": "error"}), 400

    ID = request.json["id"]
    name_th = request.json["name_th"]
    name_en = request.json["name_en"]
    province_id = request.json["province_id"]

    client = datastore.Client()
    entity = datastore.Entity(key=client.key("Amphur"))
    entity.update(
        {
            'id': ID,
            'name_th': name_th,
            'name_en': name_en,
            'province_id': province_id
        }
    )
    client.put(entity)

    return "ok"

@dashboard_bp.route("/upload/tambon", methods=["POST"])
def upload_tambon():
    if request.json["secret"] != os.environ.get('UPLOAD_SECRET'):
        return jsonify({"status": "error"}), 400

    ID = request.json["id"]
    name_th = request.json["name_th"]
    name_en = request.json["name_en"]
    zip_code = request.json["zip_code"]
    amphur_id = request.json["amphur_id"]

    client = datastore.Client()
    entity = datastore.Entity(key=client.key("Tambon"))
    entity.update(
        {
            'id': ID,
            'name_th': name_th,
            'name_en': name_en,
            'zip_code': zip_code,
            'amphur_id': amphur_id
        }
    )
    client.put(entity)

    return "ok"

