from flask import Blueprint, request, redirect, jsonify, make_response, send_file
from auth.auth import check_admin, check_roles, admin_response
from models import med_job_model, phys_model
import io

med_job_bp = Blueprint('med_job_bp', __name__)

@med_job_bp.route("/med_sup")
def med_sup():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "D01"):
        return "Unauthorized"
    
    return admin_response('med_sup.html', user_data)

@med_job_bp.route("/foot_opd")
def foot_opd():
    user_data = check_admin(request)
    if not user_data:
        return make_response(redirect("/"))
    
    if not check_roles(user_data["roles"], "D02", [1,3]):
        return "Unauthorized"
    
    return admin_response('foot_opd.html', user_data)

@med_job_bp.route("/med_jobs/upload_file", methods=["POST"])
def upload_file():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D02", [1,3]):
        return jsonify({"status": "U"}), 403
    
    if 'file' not in request.files:
        return jsonify({"status": "F", "err_message": "No file part in the request"})

    mj_id = int(request.form.get("mj_id", 0))
    pt_hn = request.form.get("pt_hn", "")
    file = request.files["file"]
    file_id = request.form.get("file_id", "")

    if mj_id == 0:
        return jsonify({"status": "F", "err_message": "Invalid job id"})

    if pt_hn == "" or file_id == "" or file.filename == "":
        return jsonify({"status": "F", "err_message": "Invalid file selection"})

    info = med_job_model.upload_file(mj_id, pt_hn, file_id, file)
    return jsonify({"status": "T", "info": info})

@med_job_bp.route("/med_jobs/download_file", methods=["POST"])
def download_file():
    user_data = check_admin(request)
    if not user_data:
        raise Exception("I")
    
    file_data, content_type = med_job_model.download_file(request.json["file_path"])
    if not file_data:
        raise Exception("File")

    return send_file(io.BytesIO(file_data), mimetype=content_type)

@med_job_bp.route("/med_jobs/get_file", methods=["POST"])
def get_file():
    user_data = check_admin(request)
    if not user_data:
        raise Exception("I")
    
    file_data, content_type = med_job_model.get_file(request.json["pt_hn"], request.json["mj_id"], request.json["file_name"])
    if not file_data:
        raise Exception("File")

    return send_file(io.BytesIO(file_data), mimetype=content_type)

@med_job_bp.route("/med_jobs/get_phys", methods=["POST"])
def get_phys():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status":"I"}), 401
    try:
        return jsonify({"status":"T", "data_list":phys_model.get(int(user_data["site_id"]))})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@med_job_bp.route("/med_jobs/create_phys", methods=["POST"])
def create_phys():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status":"I"}), 401
    try:
        phys_model.create(request.json, int(user_data["site_id"]))
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@med_job_bp.route("/med_jobs/update_phys", methods=["POST"])
def update_phys():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status":"I"}), 401
    try:
        phys_model.update(request.json, int(user_data["site_id"]))
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422

@med_job_bp.route("/med_jobs/submit", methods=["POST"])
def submit():
    user_data = check_admin(request)
    if not user_data:
        return jsonify({"status": "I"}), 401
    
    if not check_roles(user_data["roles"], "D02", [1,3]):
        return jsonify({"status": "U"}), 403
    
    try:
        med_job_model.submit(request.json, int(user_data["site_id"]))
        return jsonify({"status":"T"})
    except Exception as e:
        return jsonify({"status":"F", "err_message":str(e)}), 422