# config/firebase.py
import os
import json
import firebase_admin
from firebase_admin import credentials

def init_firebase():
    try:
        if firebase_admin._apps:
            return

        firebase_json = os.environ.get("FIREBASE_JSON")
        if not firebase_json:
            raise RuntimeError("FIREBASE_JSON env var missing")

        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)

        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized")

    except Exception as e:
        print("❌ Firebase init failed:", str(e))
        raise
