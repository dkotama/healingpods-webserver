from flask import Blueprint

patient = Blueprint('patient ', __name__)


@patient.route("/register")
def register():
