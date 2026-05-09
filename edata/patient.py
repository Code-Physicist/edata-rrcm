from flask import Blueprint, request, redirect, jsonify, make_response, send_file
from auth.auth import check_admin, check_roles, admin_response
from models import patient_model
import io

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route("/patients")
def patients():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "D01"):
        return "Unauthorized"

    return admin_response('patients.html', user_data)

@patient_bp.route("/patients/get", methods=["POST"])
def get_patients():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    search_param = request.json["search_param"]
    search_text = request.json["search_text"]
    if search_text != "":
        return jsonify({"status": "T", "data_list": patient_model.search(search_param, search_text, user_data["site_id"])})
    
    return jsonify({"data_list": patient_model.get(user_data["site_id"])})

@patient_bp.route("/patients/get2", methods=["POST"])
def get_patients2():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    search_text = request.json["search_text"]
    if search_text != "":
        return jsonify({"status": "T", "data_list": patient_model.search("full_name", search_text, user_data["site_id"])})
    
    return jsonify({"data_list": []})

@patient_bp.route("/patients/get_photo", methods=["POST"])
def get_photo():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401

    try:
        hn = request.json["hn"]
        image_data, mime_type = patient_model.get_photo(hn)
        image_stream = io.BytesIO(image_data)
        return send_file(image_stream, mimetype=mime_type)
    except:
        return jsonify({"status": "F"}), 404
    

@patient_bp.route("/patients/create", methods=["POST"])
def patient():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D01"):
        return jsonify({"status": "U"}), 403

    try:
        patient_model.create(request.json, int(user_data["site_id"]))
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@patient_bp.route("/patients/update", methods=["POST"])
def update_patient():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D01"):
        return jsonify({"status": "U"}), 403

    try:
        patient_model.update(request.json, user_data["site_id"])
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422