FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

# 🔒 Force wheels only (no source builds)
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "180"]
