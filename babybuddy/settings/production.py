"""Environment-driven production settings.

All configuration comes from environment variables so a single image can
be reused across hosts. Expected environment:

* ``SECRET_KEY`` (required)
* ``DATABASE_URL`` (default: sqlite at ``../data/db.sqlite3``)
* ``ALLOWED_HOSTS`` (comma-separated, default: ``*``)
* ``CSRF_TRUSTED_ORIGINS`` (comma-separated, optional)
* ``MEDIA_ROOT`` (default: ``../data/media``)
* ``MEDIA_URL`` (default: ``/media/``)
* ``DEBUG`` (default: off)
"""
import os
import dj_database_url

from .base import *  # noqa: F401,F403

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ.get("DEBUG", "").lower() in {"1", "true", "yes"}

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "*").split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, '../data/db.sqlite3')}",  # noqa: F405
        conn_max_age=600,
    )
}

MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(BASE_DIR, "../data/media"))  # noqa: F405
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
