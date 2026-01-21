import numpy as np

# ==============================
# MATCHING THRESHOLDS
# ==============================
STRONG_MATCH_THRESHOLD = 0.75   # definite same person
REVIEW_MATCH_THRESHOLD = 0.65   # possible same person


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)

    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0

    return float(np.dot(a, b) / denom)


def find_matches(detected_embeddings, enrolled_users):
    """
    For each detected face:
      - Compare against ALL stored embeddings of each user
      - Take the BEST similarity per user
      - Decide match level based on confidence bands
    """

    results = []

    for face_emb in detected_embeddings:
        for user in enrolled_users:
            best_score = 0.0

            for stored_emb in user["embeddings"]:
                score = cosine_similarity(face_emb, stored_emb)
                if score > best_score:
                    best_score = score

            # ------------------------------
            # Decision logic
            # ------------------------------
            if best_score >= STRONG_MATCH_THRESHOLD:
                results.append({
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "confidence": round(best_score, 3),
                    "match_level": "strong"
                })

            elif best_score >= REVIEW_MATCH_THRESHOLD:
                results.append({
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "confidence": round(best_score, 3),
                    "match_level": "review"
                })

            # else: ignore (no entry)

    return results
