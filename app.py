from flask import Flask
from flask_cors import CORS

from config.firebase import init_firebase
from api.enroll import enroll_bp
from api.scan import scan_bp
from api.health import health_bp

app = Flask(__name__)
CORS(app)

# Register routes FIRST
app.register_blueprint(enroll_bp)
app.register_blueprint(scan_bp)
app.register_blueprint(health_bp)

# ✅ IMPORTANT: Initialize Firebase AFTER app starts
@app.before_first_request
def startup():
    init_firebase()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
