from flask import Blueprint, request, redirect, jsonify, make_response
from auth.auth import check_admin, check_roles, admin_response
from models import site_model

site_bp = Blueprint('site_bp', __name__)

@site_bp.route("/sites")
def sites():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "A01"):
        return "Unauthorized"

    return admin_response('sites.html', user_data)

@site_bp.route("/sites/get", methods=["POST"])
def get_sites():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    return jsonify({"status": "T", "data_list": site_model.get()})

@site_bp.route("/sites/create", methods=["POST"])
def create_site():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        site_model.create(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@site_bp.route("/sites/update", methods=["POST"])
def update_site():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        site_model.update(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422