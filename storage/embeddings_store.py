from firebase_admin import firestore
from privacy.encryption import encrypt, decrypt

_db = None

def get_db():
    global _db
    if _db is None:
        _db = firestore.client()
    return _db

def save_user_embeddings(user_id, username, embeddings, quality):
    db = get_db()
    db.collection("fpp_users").document(user_id).set({
        "username": username,
        "embeddings": encrypt(embeddings),
        "embedding_version": "v1",
        "quality": quality,
        "status": "ACTIVE",
        "created_at": firestore.SERVER_TIMESTAMP
    })

def load_all_embeddings():
    db = get_db()
    users = []
    docs = db.collection("fpp_users").where("status", "==", "ACTIVE").stream()
    for d in docs:
        data = d.to_dict()
        users.append({
            "user_id": d.id,
            "username": data["username"],
            "embeddings": decrypt(data["embeddings"])
        })
    return users
