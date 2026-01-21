from flask import Blueprint, jsonify
import os
import psutil
import time

health_bp = Blueprint("health", __name__)

START_TIME = time.time()

@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "FPP-ML",
        "env": os.getenv("ENV", "dev"),
        "uptime_seconds": int(time.time() - START_TIME),
        "memory_mb": round(psutil.virtual_memory().used / (1024 * 1024), 2),
        "cpu_percent": psutil.cpu_percent(interval=0.1)
    })
