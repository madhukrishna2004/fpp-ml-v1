from firebase_admin import firestore
from datetime import datetime

def log_scan(post_id, media_url):
    db = firestore.client()
    db.collection("fpp_scan_logs").add({
        "event": "SCAN",
        "post_id": post_id,
        "media_url": media_url,
        "timestamp": datetime.utcnow()
    })
