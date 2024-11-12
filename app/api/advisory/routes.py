from flask import Blueprint, jsonify

bp = Blueprint("advisory", __name__)

@bp.route("/", methods=["GET"])
def check_advisory():
    snow_depth = 50  # Placeholder
    threshold = 10
    return jsonify({"advisory": snow_depth > threshold})