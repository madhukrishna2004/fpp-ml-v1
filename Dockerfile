# =========================
# Single-stage (no apt, no GPG)
# =========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Upgrade pip tooling
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python deps only
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# App Runner port
EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
