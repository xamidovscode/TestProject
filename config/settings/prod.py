from .base import *
DEBUG = False

ALLOWED_HOSTS = [
    "mahamatjanov.uz",
    "www.mahamatjanov.uz",
]

CSRF_TRUSTED_ORIGINS = [
    "https://mahamatjanov.uz",
    "https://www.mahamatjanov.uz",
]

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True
#
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"