from .base import *
DEBUG = False

ALLOWED_HOSTS = ["mahamatjanov.uz","www.mahamatjanov.uz"]

CORS_ALLOWED_ORIGINS = [
    "http://192.168.1.148:3001",
    "http://localhost:3001",
    "https://mahamatjanov.uz",
    "https://www.mahamatjanov.uz",
    "https://lorry-copy.vercel.app/",
]

EMAIL_TIMEOUT = 5

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"