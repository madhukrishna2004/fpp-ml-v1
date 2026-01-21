from flask import Blueprint, request, jsonify
from config.security import verify_firebase_user
from core.embedder import embed_faces
from core.matcher import find_matches
from storage.media_loader import load_image_from_url
from storage.embeddings_store import load_all_embeddings
from logs.scan_log import log_scan
from logs.match_log import log_match
import uuid

scan_bp = Blueprint("scan", __name__, url_prefix="/fpp")


@scan_bp.route("/scan", methods=["POST"])
def scan():
    user = verify_firebase_user(request)
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid_payload"}), 400

    media_url = data.get("media_url")
    post_id = data.get("post_id", str(uuid.uuid4()))

    if not media_url:
        return jsonify({"error": "media_url_required"}), 400

    # ================= VIDEO =================
    if media_url.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        try:
            from core.video_scanner import scan_video

            enrolled_users = load_all_embeddings()
            matches = scan_video(media_url, enrolled_users)

            try:
                log_scan(post_id, media_url)
                for m in matches:
                    log_match(post_id, m)
            except Exception:
                pass

            return jsonify({
                "media_type": "video",
                "matches": matches,
                "status": "completed"
            })

        except Exception as e:
            return jsonify({
                "error": "video_scan_failed",
                "message": str(e)
            }), 500

    # ================= IMAGE =================
    try:
        image = load_image_from_url(media_url)
        detected_embeddings = embed_faces([image])

        enrolled_users = load_all_embeddings()
        matches = find_matches(detected_embeddings, enrolled_users)

        try:
            log_scan(post_id, media_url)
            for m in matches:
                log_match(post_id, m)
        except Exception:
            pass

        return jsonify({
            "media_type": "image",
            "faces_detected": len(detected_embeddings),
            "matches": matches,
            "status": "completed"
        })

    except Exception as e:
        return jsonify({
            "error": "image_scan_failed",
            "message": str(e)
        }), 500
