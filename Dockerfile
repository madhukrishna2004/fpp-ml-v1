# =========================
# Stage 1 — Builder
# =========================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps for building ML libs
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

# Upgrade pip tools
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

# Install Python deps into /install (not system)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# Stage 2 — Runtime
# =========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Runtime system deps only
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed python packages
COPY --from=builder /install /usr/local

# Copy app code
COPY . .

# 🔴 MUST match App Runner port
EXPOSE 8080

# Gunicorn entrypoint (App Runner compatible)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
