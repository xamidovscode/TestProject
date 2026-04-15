import random
from django.core.mail import send_mail
from django.conf import settings

def generate_auth_code():
    # code =  str(random.randint(100000, 999999))
    return 777777



def send_verify_code(email, code):
    send_mail(
        subject="Tasdiqlash kodi",
        message=f"Sizning kodingiz {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

