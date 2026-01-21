from firebase_admin import firestore
from datetime import datetime

_db = None

def get_db():
    global _db
    if _db is None:
        _db = firestore.client()
    return _db

def log_enrollment(user_id, username, quality):
    db = get_db()
    db.collection("fpp_enrollment_logs").add({
        "user_id": user_id,
        "username": username,
        "quality": quality,
        "timestamp": datetime.utcnow(),
        "event": "ENROLLMENT"
    })
