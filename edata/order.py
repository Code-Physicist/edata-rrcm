from flask import Blueprint, request, redirect, jsonify, make_response
from auth.auth import check_admin, check_roles, admin_response
from models import order_model, job_model
import io

order_bp = Blueprint('order_bp', __name__)

@order_bp.route("/orders")
def orders():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "D02"):
        return "Unauthorized"
    
    return admin_response('orders.html', user_data)

@order_bp.route("/orders/create", methods=["POST"])
def create():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D02"):
        return jsonify({"status": "U"}), 403

    try:
        return jsonify({"status":"T", "order": order_model.create(request.json,  int(user_data["site_id"]))})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@order_bp.route("/orders/submit", methods=["POST"])
def submit():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D02"):
        return jsonify({"status": "U"}), 403

    try:
        order_model.submit(int(request.json["order_id"]))
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@order_bp.route("/orders/get", methods=["POST"])
def get():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        data_list, route_dict = order_model.get(int(request.json["status"]), int(user_data["site_id"]))
        return jsonify({"status": "T", "data_list": data_list, "route_dict": route_dict})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@order_bp.route("/orders/create_job", methods=["POST"])
def create_job():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        job_model.create(request.json, int(user_data["site_id"]))
        return jsonify({"status": "T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@order_bp.route("/orders/delete_job", methods=["POST"])
def delete_job():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        job_model.delete(int(request.json["job_id"]))
        return jsonify({"status": "T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@order_bp.route("/orders/get_jobs", methods=["POST"])
def get_jobs():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        return jsonify({"status": "T", "data_list": job_model.get(request.json["lot_id"], int(user_data["site_id"]))})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@order_bp.route("/orders/get_next_lot", methods=["POST"])
def get_next_lot():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        return jsonify({"status": "T", "next_lot": order_model.get_next_lot(int(user_data["site_id"]))})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422
