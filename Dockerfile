FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt


FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=babybuddy.settings.production \
    PORT=8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY . .

# Directory for the SQLite DB + uploaded media, meant to be a bind mount.
RUN mkdir -p /data/media && chown -R nobody:nogroup /data

ENV DATABASE_URL=sqlite:////data/db.sqlite3 \
    MEDIA_ROOT=/data/media

# Collect static files at build time (uses the local temp DB env var).
RUN DJANGO_SETTINGS_MODULE=babybuddy.settings.production \
    DATABASE_URL=sqlite:///tmp/build.sqlite3 \
    SECRET_KEY=build-time-only-not-used \
    python manage.py collectstatic --noinput || true

EXPOSE 8000

# Migrate + start gunicorn.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn babybuddy.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --timeout 60 --access-logfile - --error-logfile -"]
