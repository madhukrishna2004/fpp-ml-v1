import os
import json
import firebase_admin
from firebase_admin import credentials

def init_firebase():
    # Prevent re-initialization
    if firebase_admin._apps:
        return

    firebase_json = os.environ.get("FIREBASE_JSON")

    if not firebase_json:
        raise RuntimeError("FIREBASE_JSON environment variable not set")

    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred)
