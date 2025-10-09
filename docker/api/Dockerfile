FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/certs && \
    openssl genpkey -algorithm RSA -out /app/certs/jwt-private.pem -pkeyopt rsa_keygen_bits:2048 && \
    echo "Private key generated" && \
    openssl pkey -in /app/certs/jwt-private.pem -pubout -out /app/certs/jwt-public.pem && \
    echo "Public key generated"

RUN cp .env.example .env || true


