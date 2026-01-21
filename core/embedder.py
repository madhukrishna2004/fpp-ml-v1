import base64
import cv2
import numpy as np
import requests
from core.face_detector import detect_faces
from config.settings import MAX_FACES_PER_SCAN


# ===============================
# SAFE DECODERS
# ===============================

def decode_base64_image(b64: str):
    try:
        if len(b64) > 10_000_000:  # ~7.5MB
            return None

        img_bytes = base64.b64decode(b64)
        arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None


def embed_faces(images):
    """
    images:
    - base64 strings (Flutter enroll)
    - numpy arrays (scan)
    """
    embeddings = []

    for item in images:
        if len(embeddings) >= MAX_FACES_PER_SCAN:
            break

        if isinstance(item, str):
            img = decode_base64_image(item)
        elif isinstance(item, np.ndarray):
            img = item
        else:
            continue

        if img is None:
            continue

        faces = detect_faces(img)
        if not faces:
            continue

        for face in faces:
            if len(embeddings) >= MAX_FACES_PER_SCAN:
                break

            emb = getattr(face, "embedding", None)
            if emb is not None:
                embeddings.append(emb.tolist())

    return embeddings
