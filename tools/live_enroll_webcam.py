import cv2
import base64
import requests
import time
import math
import sys

# ===============================
# CONFIG (PRODUCTION-READY)
# ===============================

# 🔗 Firebase Function (NOT ML DIRECT)
ENROLL_API_URL = "https://us-central1-miyraa.cloudfunctions.net/fppEnroll"

CAPTURE_SECONDS = 1.2
CIRCLE_RADIUS = 140

CENTER_TOLERANCE = 45
TURN_OFFSET = 50
PROFILE_WIDTH_RATIO = 0.78

REQUEST_TIMEOUT = 20

# ===============================
# UX FLOW (MATCHES FLUTTER)
# ===============================

STEPS = [
    ("LOOK STRAIGHT", "center"),
    ("TURN FACE LEFT", "left"),
    ("TURN FACE RIGHT", "right"),
]

captured_frames = []

# ===============================
# HELPERS
# ===============================

def frame_to_base64(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")

def draw_center_guide(frame, cx, cy):
    cv2.circle(frame, (cx, cy), CIRCLE_RADIUS, (255, 255, 255), 2)

def draw_instruction(frame, text):
    cv2.putText(
        frame,
        text,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.3,
        (0, 255, 0),
        3
    )

def draw_progress(frame, cx, cy, progress):
    angle = int(360 * progress)
    cv2.ellipse(
        frame,
        (cx, cy),
        (CIRCLE_RADIUS + 14, CIRCLE_RADIUS + 14),
        0,
        0,
        angle,
        (0, 255, 0),
        6
    )

# ===============================
# FACE DETECTOR (FAST & SAFE)
# ===============================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("❌ Webcam not available")
    sys.exit(1)

print("🚀 FPP Live Enrollment Started")
time.sleep(1)

# ===============================
# MAIN LOOP
# ===============================

for label, mode in STEPS:
    print(f"[STEP] {label}")
    stable_start = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        face_valid = False

        for (x, y, fw, fh) in faces:
            face_cx = x + fw // 2
            face_width_ratio = fw / w
            dist = math.dist((face_cx, cy), (cx, cy))

            # ===============================
            # POSE VALIDATION
            # ===============================
            pose_ok = False

            if mode == "center":
                pose_ok = abs(face_cx - cx) < CENTER_TOLERANCE

            elif mode == "left":
                pose_ok = face_cx > cx + TURN_OFFSET or face_width_ratio < PROFILE_WIDTH_RATIO

            elif mode == "right":
                pose_ok = face_cx < cx - TURN_OFFSET or face_width_ratio < PROFILE_WIDTH_RATIO

            if dist < CIRCLE_RADIUS and pose_ok:
                face_valid = True
                cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 255, 0), 2)

        draw_center_guide(frame, cx, cy)
        draw_instruction(frame, label)

        if face_valid:
            if stable_start is None:
                stable_start = time.time()

            elapsed = time.time() - stable_start
            progress = min(elapsed / CAPTURE_SECONDS, 1.0)
            draw_progress(frame, cx, cy, progress)

            if progress >= 1.0:
                captured_frames.append(frame_to_base64(frame))
                print(f"✅ Captured: {label}")
                time.sleep(0.6)
                break
        else:
            stable_start = None

        cv2.imshow("FPP Live Enrollment", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            cap.release()
            cv2.destroyAllWindows()
            print("❌ Enrollment cancelled")
            sys.exit(0)

cap.release()
cv2.destroyAllWindows()

# ===============================
# SEND TO BACKEND
# ===============================

print("📡 Sending enrollment data...")

payload = {
    "images": captured_frames
}

try:
    response = requests.post(
        ENROLL_API_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )

    print("✅ Status:", response.status_code)
    print(response.json())

except Exception as e:
    print("❌ Enrollment failed:", str(e))
