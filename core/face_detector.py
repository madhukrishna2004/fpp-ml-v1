import insightface
import numpy as np

_model = None

def get_model():
    """
    Lazy-load InsightFace model (singleton).
    """
    global _model
    if _model is None:
        _model = insightface.app.FaceAnalysis(name="buffalo_l")
        _model.prepare(
            ctx_id=0,           # CPU
            det_size=(640, 640)
        )
    return _model


def detect_faces(image):
    """
    Always returns a LIST.
    Never returns None.
    Never crashes on invalid input.
    """

    # 🔐 Guard: invalid image
    if image is None:
        return []

    if not isinstance(image, np.ndarray):
        return []

    # 🔐 Guard: image shape invalid
    if image.ndim < 2:
        return []

    try:
        model = get_model()
        faces = model.get(image)

        # 🔐 InsightFace may return None
        if faces is None:
            return []

        # 🔐 Ensure list
        return list(faces)

    except Exception:
        # In production we NEVER crash ML pipeline
        return []
