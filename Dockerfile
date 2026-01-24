FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# --------------------------------------------------
# 1️⃣ System deps REQUIRED for insightface
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
# 3️⃣ Install BUILD-TIME deps for insightface
# --------------------------------------------------
RUN pip install Cython

# --------------------------------------------------
# 4️⃣ Copy requirements (cache layer)
# --------------------------------------------------
COPY requirements.txt .

# --------------------------------------------------
# 5️⃣ Install SAFE wheels-only deps
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
# 6️⃣ Install InsightFace (SOURCE BUILD)
# --------------------------------------------------
RUN pip install insightface==0.7.3 --no-build-isolation

# --------------------------------------------------
# 7️⃣ Copy application code
# --------------------------------------------------
COPY . .

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
