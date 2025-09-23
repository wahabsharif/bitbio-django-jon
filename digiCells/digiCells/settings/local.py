from .base import *
import os

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Override DEBUG for local development
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*", "0.0.0.0"]

# Database configuration
# Use PostgreSQL in Docker, SQLite for local development
if os.environ.get("DATABASE_URL") and dj_database_url:
    DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Static files configuration for Docker
STATIC_ROOT = os.path.join(BASE_DIR.parent, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "digiCells_core", "static"),
]
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")

# Security settings for Docker
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-5xqlc1c6bq(rg9^sf0*4e^&=n-yo*-n#zqynp1t7thh2l5z1de"
)
