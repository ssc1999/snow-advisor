from flask import Blueprint, jsonify, request
from ...db.mongodb import get_all_resorts, get_resorts_cache, add_resort_to_all_resorts, delete_resort_from_all_resorts

bp = Blueprint("resorts", __name__)

@bp.route("/all", methods=["GET"])
def fetch_all_resorts():
    all_resorts = get_all_resorts()
    return jsonify(all_resorts), 200

@bp.route("/cache", methods=["GET"])
def fetch_resorts():
    resorts = get_resorts_cache()
    return jsonify(resorts), 200

@bp.route("", methods=["POST"])
def add_resort():
    resort_data = request.get_json()
    if not resort_data or "resort_name" not in resort_data:
        return jsonify({"error": "Invalid input. 'resort_name' is required."}), 400

    result = add_resort_to_all_resorts(resort_data)
    if result:
        return jsonify({"message": "Resort added or updated successfully.", "result": str(result)}), 201
    else:
        return jsonify({"message": "No change made."}), 200
    
@bp.route("", methods=["DELETE"])
def delete_resort():
    resort_data = request.get_json()
    if not resort_data or "resort_name" not in resort_data:
        return jsonify({"error": "Invalid input. 'resort_name' is required."}), 400

    result = delete_resort_from_all_resorts(resort_data["resort_name"])
    if result:
        return jsonify({"message": "Resort deleted successfully."}), 200
    else:
        return jsonify({"error": "Resort not found."}), 404