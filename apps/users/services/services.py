import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction

from .redis_client import redis_client

User = get_user_model()

PENDING_REGISTRATION_TTL = 120


class VerificationError(Exception):
    pass


class PendingRegistrationExpiredError(VerificationError):
    pass


class VerificationCodeExpiredError(VerificationError):
    pass


class InvalidVerificationCodeError(VerificationError):
    pass


class UserAlreadyExistsError(VerificationError):
    pass


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_pending_user_key(email: str) -> str:
    return f"pending_user:{normalize_email(email)}"


def get_verify_code_key(email: str) -> str:
    return f"verify_code:{normalize_email(email)}"


def save_pending_registration(email: str, full_name: str, password: str) -> None:
    email = normalize_email(email)
    full_name = full_name.strip()

    hashed_password = make_password(password)

    data = {
        "email": email,
        "full_name": full_name,
        "password": hashed_password,
    }

    redis_client.setex(
        get_pending_user_key(email),
        PENDING_REGISTRATION_TTL,
        json.dumps(data),
    )


def get_pending_registration(email: str) -> dict | None:
    email = normalize_email(email)

    data = redis_client.get(get_pending_user_key(email))
    if not data:
        return None

    return json.loads(data)


def delete_pending_registration(email: str) -> None:
    email = normalize_email(email)
    redis_client.delete(get_pending_user_key(email))


def get_verification_code(email: str) -> str | None:
    email = normalize_email(email)
    return redis_client.get(get_verify_code_key(email))


def delete_verification_code(email: str) -> None:
    email = normalize_email(email)
    redis_client.delete(get_verify_code_key(email))


def clear_verification_data(email: str) -> None:
    email = normalize_email(email)
    redis_client.delete(
        get_pending_user_key(email),
        get_verify_code_key(email),
    )


def verify_email_registration(data: dict) -> User:
    email = normalize_email(data["email"])
    code = data["code"].strip()

    pending_user = get_pending_registration(email)
    if pending_user is None:
        raise PendingRegistrationExpiredError(
            "Pending registration not found or expired."
        )

    stored_code = get_verification_code(email)
    if stored_code is None:
        raise VerificationCodeExpiredError(
            "Verification code not found or expired."
        )

    if stored_code != code:
        raise InvalidVerificationCodeError("Invalid verification code.")

    if User.objects.filter(email=email).exists():
        clear_verification_data(email)
        raise UserAlreadyExistsError("User already exists.")

    with transaction.atomic():
        user = User.objects.create(
            email=pending_user["email"],
            full_name=pending_user["full_name"],
            password=pending_user["password"],
            is_verified=True,
            is_active=True,
        )

    clear_verification_data(email)
    return user