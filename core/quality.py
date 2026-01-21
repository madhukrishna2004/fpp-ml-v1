def face_quality(embeddings):
    if not embeddings:
        return 0.0
    return min(1.0, len(embeddings) / 3)
