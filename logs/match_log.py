from firebase_admin import firestore
from datetime import datetime

def log_match(post_id, match):
    db = firestore.client()
    db.collection("fpp_match_logs").add({
        "event": "MATCH_FOUND",
        "post_id": post_id,
        "matched_user": match["user_id"],
        "confidence": match["confidence"],
        "status": "PENDING",
        "timestamp": datetime.utcnow()
    })
