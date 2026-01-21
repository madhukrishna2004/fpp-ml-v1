import cv2
import tempfile
import requests
import os
from core.embedder import embed_faces
from core.matcher import find_matches


FRAME_INTERVAL_SEC = 1       # sample every 1 second
MAX_FRAMES = 20              # hard safety cap


def scan_video(video_url, enrolled_users):
    """
    Scans a video for faces and matches them against enrolled users.
    Returns aggregated match results.
    """

    # ----------------------------
    # Download video temporarily
    # ----------------------------
    resp = requests.get(video_url, stream=True, timeout=15)
    resp.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        for chunk in resp.iter_content(chunk_size=8192):
            tmp.write(chunk)
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25

    frame_interval = int(fps * FRAME_INTERVAL_SEC)
    frame_count = 0
    sampled = 0

    all_matches = []

    while cap.isOpened() and sampled < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # 🔹 Extract embeddings from this frame
            embeddings = embed_faces([frame])

            if embeddings:
                matches = find_matches(embeddings, enrolled_users)
                all_matches.extend(matches)

            sampled += 1

        frame_count += 1

    cap.release()
    os.unlink(video_path)

    # ----------------------------
    # Aggregate matches
    # ----------------------------
    return aggregate_video_matches(all_matches)


def aggregate_video_matches(matches):
    """
    Aggregates frame-level matches into video-level decisions.
    """

    per_user = {}

    for m in matches:
        uid = m["user_id"]
        score = m["confidence"]

        if uid not in per_user:
            per_user[uid] = {
                "user_id": uid,
                "username": m["username"],
                "scores": []
            }

        per_user[uid]["scores"].append(score)

    results = []

    for user in per_user.values():
        scores = sorted(user["scores"], reverse=True)

        max_score = scores[0]
        avg_top3 = sum(scores[:3]) / min(3, len(scores))

        if max_score >= 0.75:
            level = "strong"
        elif avg_top3 >= 0.65:
            level = "review"
        else:
            continue

        results.append({
            "user_id": user["user_id"],
            "username": user["username"],
            "max_confidence": round(max_score, 3),
            "avg_confidence": round(avg_top3, 3),
            "match_level": level
        })

    return results
