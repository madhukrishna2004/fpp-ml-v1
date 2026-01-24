FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# ---- base tools (NO apt needed) ----
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

# 1️⃣ Install all SAFE wheels-only deps (exclude insightface)
RUN pip install --only-binary=:all: \
    flask \
    flask-cors \
    gunicorn \
    opencv-python-headless \
    numpy<2.0 \
    onnxruntime \
    requests \
    firebase-admin \
    cryptography \
    psutil \
    packaging \
    setuptools \
    wheel

# 2️⃣ Install InsightFace ALONE (allow source build)
RUN pip install insightface==0.7.3 --no-build-isolation

COPY . .

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
