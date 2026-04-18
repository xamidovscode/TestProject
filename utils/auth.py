import random
import requests
from django.conf import settings

def generate_auth_code():
    code =  str(random.randint(100000, 999999))
    return code


class BrevoEmailError(Exception):
    pass


def send_verify_code(email: str, code: str) -> None:
    if not settings.BREVO_API_KEY:
        raise BrevoEmailError("BREVO_API_KEY topilmadi.")

    if not settings.BREVO_SENDER_EMAIL:
        raise BrevoEmailError("BREVO_SENDER_EMAIL topilmadi.")

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }
    payload = {
        "sender": {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL,
        },
        "to": [
            {
                "email": email,
            }
        ],
        "subject": "Tasdiqlash kodi",
        "htmlContent": f"""
        <html>
            <body>
                <h2>Tasdiqlash kodi</h2>
                <p>Sizning tasdiqlash kodingiz:</p>
                <h1>{code}</h1>
            </body>
        </html>
        """,
        "textContent": f"Sizning tasdiqlash kodingiz: {code}",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=15)

    if response.status_code not in (200, 201, 202):
        raise BrevoEmailError(
            f"Brevo email yuborishda xato: {response.status_code} - {response.text}"
        )