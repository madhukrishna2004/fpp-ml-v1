from flask import Flask
from flask_cors import CORS

from config.firebase import init_firebase
from api.enroll import enroll_bp
from api.scan import scan_bp
from api.health import health_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    # ✅ Register routes FIRST (no Firebase here)
    app.register_blueprint(enroll_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(health_bp)

    # ✅ Initialize Firebase lazily (App Runner safe)
    @app.before_first_request
    def startup():
        init_firebase()

    return app


# ✅ App Runner + Gunicorn entrypoint
app = create_app()


# ✅ Local development only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
