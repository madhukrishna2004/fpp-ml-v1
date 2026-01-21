import requests
import cv2
import numpy as np
from urllib.parse import urlparse

# ===============================
# SECURITY LIMITS
# ===============================
ALLOWED_DOMAINS = [
    "firebasestorage.googleapis.com",
    "storage.googleapis.com",
    "127.0.0.1",          # local dev
    "localhost"
]

MAX_IMAGE_MB = 10
TIMEOUT_SEC = 8


def _validate_url(url: str):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid URL scheme")

    host = parsed.hostname
    if not host or not any(host.endswith(d) for d in ALLOWED_DOMAINS):
        raise ValueError("URL domain not allowed")


def load_image_from_url(url: str):
    _validate_url(url)

    response = requests.get(
        url,
        timeout=TIMEOUT_SEC,
        stream=True
    )
    response.raise_for_status()

    content_length = int(response.headers.get("Content-Length", 0))
    if content_length > MAX_IMAGE_MB * 1024 * 1024:
        raise ValueError("Image too large")

    data = response.content
    image_array = np.frombuffer(data, np.uint8)

    # Try standard decode
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Fallback for PNG / alpha images
    if image is None:
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        if image is None:
            raise ValueError("Invalid image format")

        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    return image
