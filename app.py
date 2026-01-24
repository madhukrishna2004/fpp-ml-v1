from flask import Flask
from flask_cors import CORS

from config.firebase import init_firebase
from api.enroll import enroll_bp
from api.scan import scan_bp
from api.health import health_bp

firebase_initialized = False


def create_app():
    app = Flask(__name__)
    CORS(app)

    # ✅ Root route (prevents 404 confusion)
    @app.route("/")
    def root():
        return {
            "service": "miyraa-fpp-ml",
            "status": "running"
        }

    # ✅ Health MUST be ultra-light
    app.register_blueprint(health_bp)

    # ✅ Register heavy routes after
    app.register_blueprint(enroll_bp)
    app.register_blueprint(scan_bp)

    return app


app = create_app()


# ✅ Initialize Firebase SAFELY (once, guarded)
def init_once():
    global firebase_initialized
    if not firebase_initialized:
        init_firebase()
        firebase_initialized = True


# ✅ Wrap Gunicorn startup
init_once()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
