from flask import Blueprint, request, redirect, jsonify, make_response
from auth.auth import check_admin, check_roles, admin_response
from models import user_model

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/users")
def users():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "A01"):
        return "Unauthorized"

    return admin_response('users.html', user_data)

@user_bp.route("/users/get", methods=["POST"])
def get_users():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    return jsonify({"status": "T", "data_list": user_model.get()})

@user_bp.route("/users/create", methods=["POST"])
def create_user():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        user_model.create(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)})

@user_bp.route("/users/update", methods=["POST"])
def update_user():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        user_model.update(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)})
