import os
import hashlib
import json
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, redirect, jsonify, render_template, make_response
from google.cloud import datastore
import jwt

JWT_SECRET = "ezJydWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV7"
RRCM_CK = "rrcm_ck"
PATH_DICT = {
    "A01": "/operations",
    "D01": "/patients",
    "D02": "/foot_opd",
}

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/")
def index():
    user_data = check_admin(request)
    if user_data:
        role_dict = user_data["roles"]
        for key in sorted(role_dict.keys()):
            return make_response(redirect(PATH_DICT[key]))
        
        # No authorization, force log out
        return make_response(redirect("/logout"))
    
    response = make_response(render_template('login.html'))
    prevent_back_history(response) 
    return response

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = hashlib.md5(request.json["password"].encode('UTF-8')).hexdigest()

    client = datastore.Client()
    query = client.query(kind='User')
    query.add_filter("username", "=", username)
    query.add_filter("password", "=", password)
    user = next(query.fetch(1), None)
    if not user:
        return jsonify({"status": "I"})

    roles = user["roles"]
    role_dict = {}
    for role in roles:
        role_dict[role["opn_id"]] = role["role_type"]
    
    site_id = int(user["site_id"]) 
    site = client.get(client.key("Site", site_id))
    
    payload = {
        "user_id": int(user.key.id_or_name),
        "username": user["username"],
        "name": ' '.join([s for s in [user["prefix"], user["first_name"], user["last_name"]] if s]),
        "roles": role_dict,
        "site_id": site_id,
        "site_name": site["name"]
    }
    
    jwt_token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm="HS256")
    res = make_response({"status":"T"})
    res.set_cookie(RRCM_CK, jwt_token)
    return res

@auth_bp.route("/logout")
def logout():
    res = make_response(redirect("/"))
    res.set_cookie(RRCM_CK, "")
    return res

@auth_bp.route("/auth/test_user")
def test_user():
    user_data = check_admin(request)
    return jsonify(user_data)

def admin_response(html_template, user_data):
    response = make_response(render_template(html_template, 
            admin_id = user_data["user_id"], 
            username = user_data["username"],
            name = user_data["name"],
            roles = user_data["roles"],
            site_id = user_data["site_id"],
            site_name = user_data["site_name"]
        ))

    prevent_back_history(response)
    return response

def check_admin(req):
    try:
        if not RRCM_CK in req.cookies: return None
    
        token = req.cookies.get(RRCM_CK)
        data = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"])
        if not all(k in data for k in ("user_id", "username", "name", "roles", "site_id", "site_name")):
            return None

        return data
    except:
        return None

def check_roles(roles, code, role_list=[]):
    chk = code in roles
    if chk and role_list:
        chk = False
        for r in role_list:
            chk |= (roles[code] == r)

    return chk

def prevent_back_history(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')