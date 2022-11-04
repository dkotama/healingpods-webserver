from flask import Blueprint

walkingpad = Blueprint('walkingpad', __name__)


@walkingpad.route("/walkingpad")
def index():
    return "Walkingpad route"