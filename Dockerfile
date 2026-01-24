# =========================
# Stage 1 — Builder
# =========================
FROM python:3.11-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# ---- System deps for building Python wheels ----
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /install

# Upgrade pip tooling
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

# Install Python deps into /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# Stage 2 — Runtime
# =========================
FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Runtime system deps (CPU-only InsightFace) ----
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /app

# Copy Python packages
COPY --from=builder /install /usr/local

# Copy app code
COPY . .

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
