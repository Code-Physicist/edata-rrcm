from flask import Blueprint, request, redirect, jsonify, make_response, send_file
from auth.auth import check_admin, check_roles, admin_response
from models import appt_model
import io

appt_bp = Blueprint('appt_bp', __name__)

@appt_bp.route("/appointments")
def appts():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "D01"):
        return "Unauthorized"
    
    return admin_response('appointment.html', user_data)

@appt_bp.route("/appointments/create", methods=["POST"])
def create():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D01"):
        return jsonify({"status": "U"}), 403

    try:
        appt_model.create(request.json,  int(user_data["site_id"]))
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)})

@appt_bp.route("/appointments/get", methods=["POST"])
def get():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    if "is_sup" in request.json and not request.json["is_sup"]:
        return jsonify({"data_list": appt_model.get(request.json, int(user_data["site_id"]), int(user_data["user_id"]))})
    else:
        return jsonify({"data_list": appt_model.get(request.json, int(user_data["site_id"]))})

@appt_bp.route("/appointments/check_in", methods=["POST"])
def check_in():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D02", [1,3]):
        return jsonify({"status": "U"}), 403

    try:
        med_job, file_infos = appt_model.check_in(request.json, int(user_data["site_id"]), int(user_data["user_id"]))
        return jsonify({"status": "T", "med_job": med_job, "file_infos": file_infos})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422