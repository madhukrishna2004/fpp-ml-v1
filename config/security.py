import os
import firebase_admin
from firebase_admin import auth
from flask import request

# ===============================
# Admin key (ONLY for internal tools)
# ===============================
ADMIN_API_KEY = os.getenv("FPP_ADMIN_API_KEY")

def verify_admin_key(req):
    key = req.headers.get("X-API-KEY")
    return key and key == ADMIN_API_KEY


# ===============================
# Firebase user verification (Flutter)
# ===============================
class AuthUser:
    def __init__(self, uid, email=None, name=None):
        self.uid = uid
        self.email = email
        self.name = name


def verify_firebase_user(req):
    """
    Flutter must send:
    Authorization: Bearer <firebase_id_token>
    """
    auth_header = req.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split("Bearer ")[1]

    try:
        decoded = auth.verify_id_token(token)
        return AuthUser(
            uid=decoded["uid"],
            email=decoded.get("email"),
            name=decoded.get("name") or decoded.get("email", "unknown")
        )
    except Exception:
        return None
