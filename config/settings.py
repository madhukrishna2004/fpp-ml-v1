import os

# ===============================
# ENV
# ===============================
ENV = os.getenv("ENV", "dev")  # dev | prod

# ===============================
# MATCHING
# ===============================
STRONG_MATCH_THRESHOLD = float(os.getenv("STRONG_MATCH_THRESHOLD", "0.85"))
REVIEW_MATCH_THRESHOLD = float(os.getenv("REVIEW_MATCH_THRESHOLD", "0.70"))

# ===============================
# SCAN LIMITS
# ===============================
MAX_FACES_PER_SCAN = int(os.getenv("MAX_FACES_PER_SCAN", "5"))

# ===============================
# VIDEO
# ===============================
VIDEO_FRAME_INTERVAL_SEC = int(os.getenv("VIDEO_FRAME_INTERVAL_SEC", "1"))
MAX_VIDEO_FRAMES = int(os.getenv("MAX_VIDEO_FRAMES", "20"))

# ===============================
# ENROLLMENT
# ===============================
MAX_ENROLL_IMAGES = int(os.getenv("MAX_ENROLL_IMAGES", "5"))
MIN_ENROLL_QUALITY = float(os.getenv("MIN_ENROLL_QUALITY", "0.6"))

# ===============================
# SECURITY
# ===============================
ENABLE_RATE_LIMIT = ENV == "prod"
