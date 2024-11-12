# app/api/info/routes.py
from flask import Blueprint, jsonify

bp = Blueprint("info", __name__)

@bp.route("", methods=["GET"])
def get_api_info():
    """Return general information about the Snow Advisor API."""
    api_info = {
        "name": "Snow Advisor API",
        "version": "1.0",
        "description": "An API providing real-time snow and weather data for various ski resorts.",
        "endpoints": [
            {"path": "/weather/<resort_name>", "method": "GET", "description": "Get weather data for a specific resort"},
            {"path": "/advisory", "method": "GET", "description": "Check if snow depth exceeds advisory threshold"},
            {"path": "/resorts/all", "method": "GET", "description": "Get all resorts from all_resorts collection"},
            {"path": "/resorts/cache", "method": "GET", "description": "Get all resorts from resorts cache"},
            {"path": "/resorts", "method": "POST", "description": "Add or update a resort in the database"},
            {"path": "/resorts", "method": "DELETE", "description": "Delete a resort in the database"},
        ],
        "documentation_url": "https://github.com/ssc1999/snow-advisor"
    }
    return jsonify(api_info), 200