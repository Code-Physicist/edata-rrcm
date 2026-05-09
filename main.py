import os
from flask import Flask
from auth.auth import auth_bp
from edata.dashboard import dashboard_bp
from edata.patient import patient_bp
from edata.appointment import appt_bp
from edata.med_job import med_job_bp
from edata.order import order_bp
from edata.user import user_bp
from edata.site import site_bp
from edata.operation import operation_bp
from edata.route import route_bp

from flask import Flask

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(appt_bp)
app.register_blueprint(med_job_bp)
app.register_blueprint(order_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(user_bp)
app.register_blueprint(site_bp)
app.register_blueprint(operation_bp)
app.register_blueprint(route_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))