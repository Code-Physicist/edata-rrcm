from flask import Blueprint, request, redirect, jsonify, make_response
from auth.auth import check_admin, check_roles, admin_response
from models import route_model

route_bp = Blueprint('route_bp', __name__)

@route_bp.route("/routes")
def operations():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "A01"):
        return "Unauthorized"

    return admin_response('routes.html', user_data)

@route_bp.route("/routes/get", methods=["POST"])
def get_operations():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        return jsonify({"status":"T", "data_list": route_model.get()})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@route_bp.route("/routes/create", methods=["POST"])
def create_operation():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        route_model.create(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@route_bp.route("/routes/update", methods=["POST"])
def update_operation():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "A01"):
        return jsonify({"status": "U"}), 403

    try:
        route_model.update(request.json)
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422