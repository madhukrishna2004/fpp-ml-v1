from flask import Blueprint, jsonify
from firebase_admin import firestore

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
db = firestore.client()

@admin_bp.route("/logs")
def logs():
    logs = []
    for d in db.collection("fpp_match_logs").limit(100).stream():
        logs.append(d.to_dict())
    return jsonify(logs)
