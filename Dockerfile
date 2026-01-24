FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# --------------------------------------------------
# 1️⃣ Minimal system deps REQUIRED for insightface
# (g++ is NON-NEGOTIABLE – insightface has C++ code)
# --------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# 2️⃣ Upgrade pip tooling
# --------------------------------------------------
RUN pip install --upgrade pip setuptools wheel

# --------------------------------------------------
# 3️⃣ Copy requirements (for caching)
# --------------------------------------------------
COPY requirements.txt .

# --------------------------------------------------
# 4️⃣ Install SAFE wheels-only deps (NO source builds)
# IMPORTANT: numpy version MUST be quoted
# --------------------------------------------------
RUN pip install --only-binary=:all: \
    flask \
    flask-cors \
    gunicorn \
    opencv-python-headless \
    "numpy<2.0" \
    onnxruntime \
    requests \
    firebase-admin \
    cryptography \
    psutil \
    packaging

# --------------------------------------------------
# 5️⃣ Install InsightFace separately (SOURCE BUILD)
# --------------------------------------------------
RUN pip install insightface==0.7.3 --no-build-isolation

# --------------------------------------------------
# 6️⃣ Copy application code
# --------------------------------------------------
COPY . .

# --------------------------------------------------
# 7️⃣ App Runner port
# --------------------------------------------------
EXPOSE 8080

# --------------------------------------------------
# 8️⃣ Gunicorn entrypoint
# --------------------------------------------------
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
