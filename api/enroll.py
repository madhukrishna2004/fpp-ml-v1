from flask import Blueprint, request, jsonify
from config.security import verify_firebase_user
from config.settings import MIN_ENROLL_QUALITY, MAX_ENROLL_IMAGES
from core.embedder import embed_faces
from core.quality import face_quality
from privacy.memory_guard import wipe
from storage.embeddings_store import save_user_embeddings
from logs.enrollment_log import log_enrollment

enroll_bp = Blueprint("enroll", __name__, url_prefix="/fpp")


@enroll_bp.route("/enroll", methods=["POST"])
def enroll():
    user = verify_firebase_user(request)
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid_payload"}), 400

    images = data.get("images", [])

    if not images:
        return jsonify({"error": "images_required"}), 400

    if len(images) > MAX_ENROLL_IMAGES:
        return jsonify({"error": "too_many_images"}), 413

    # 1️⃣ Extract embeddings
    embeddings = embed_faces(images)
    quality = face_quality(embeddings)

    if quality < MIN_ENROLL_QUALITY:
        return jsonify({"error": "low_face_quality"}), 422

    # 2️⃣ Save securely
    save_user_embeddings(
        user_id=user.uid,
        username=user.name,
        embeddings=embeddings,
        quality=quality
    )

    log_enrollment(user.uid, user.name, quality)

    # 3️⃣ Memory wipe
    wipe(images)
    wipe(embeddings)

    return jsonify({
        "status": "enrolled",
        "quality": round(float(quality), 3)
    })
