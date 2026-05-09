from flask import Blueprint, request, redirect, jsonify, make_response
from auth.auth import check_admin, check_roles, admin_response
from models import operation_model

operation_bp = Blueprint('operation_bp', __name__)

@operation_bp.route("/operations")
def operations():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "A01"):
        return "Unauthorized"

    return admin_response('operations.html', user_data)

@operation_bp.route("/operations/get", methods=["POST"])
def get():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        data_list = operation_model.get()
        return jsonify({"status":"T", "data_list": data_list})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@operation_bp.route("/operations/create", methods=["POST"])
def create():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        operation_model.create(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@operation_bp.route("/operations/update", methods=["POST"])
def update():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        operation_model.update(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422