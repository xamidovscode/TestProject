import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from .redis_client import redis_client

User = get_user_model()

VERIFY_CODE_TTL = 60
REGISTER_COOLDOWN_TTL = 60
REGISTER_MAX_COUNT = 3
REGISTER_LIMIT_WINDOW = 60 * 60 * 12

RESEND_COOLDOWN_TTL = 60
RESEND_MAX_COUNT = 5
RESEND_LIMIT_WINDOW = 60 * 60 * 12


class VerificationError(Exception):
    pass


class UserAlreadyExistsError(VerificationError):
    pass


class UserNotFoundError(VerificationError):
    pass


class UserAlreadyVerifiedError(VerificationError):
    pass


class VerificationCodeExpiredError(VerificationError):
    pass


class InvalidVerificationCodeError(VerificationError):
    pass


class RegisterCooldownError(VerificationError):
    pass


class RegisterLimitExceededError(VerificationError):
    pass

class ResendCooldownError(VerificationError):
    pass

class ResendLimitExceededError(VerificationError):
    pass


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_email_verify_code_key(email: str) -> str:
    return f"email_verify_code:{normalize_email(email)}"


def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))


def save_email_verification_code(email: str, code: str) -> None:
    key = get_email_verify_code_key(email)
    redis_client.setex(key, VERIFY_CODE_TTL, code)


def get_email_verification_code(email: str) -> str | None:
    key = get_email_verify_code_key(email)
    return redis_client.get(key)


def delete_email_verification_code(email: str) -> None:
    key = get_email_verify_code_key(email)
    redis_client.delete(key)


def get_register_cooldown_key(email: str) -> str:
    return f"register_cooldown:{normalize_email(email)}"


def has_register_cooldown(email: str) -> bool:
    key = get_register_cooldown_key(email)
    return redis_client.exists(key) == 1


def set_register_cooldown(email: str) -> None:
    key = get_register_cooldown_key(email)
    redis_client.setex(key, REGISTER_COOLDOWN_TTL, "1")

def get_register_count_key(email: str) -> str:
    return f"register_count:{normalize_email(email)}"

def get_register_count(email: str) -> int:
    key = get_register_count_key(email)
    value = redis_client.get(key)

    if value is None:
        return 0
    return int(value)

def has_exceeded_register_limit(email: str) -> bool:
    return get_register_count(email) >= REGISTER_MAX_COUNT

def increment_register_count(emil: str) -> None:
    key = get_register_count_key(emil)
    if redis_client.exists(key):
        redis_client.incr(key)
    else:
        redis_client.setex(key, REGISTER_LIMIT_WINDOW, 1)


def is_unverified_user_expired(user, hours: int = 24) -> bool:
    if user.is_verified:
        return False

    expiration_time = user.created_at + timedelta(hours=hours)
    return timezone.now() > expiration_time


def register_user(data: dict) -> User:
    email = normalize_email(data["email"])
    full_name = data["full_name"].strip()
    password = data["password"]

    existing_user = User.objects.filter(email=email).first()

    if existing_user and existing_user.is_verified:
        raise UserAlreadyExistsError(
            "User with this email was already verified."
        )

    if has_register_cooldown(email):
        raise RegisterCooldownError(
            "Please wait before requesting another verification code."
        )

    if has_exceeded_register_limit(email):
        raise RegisterLimitExceededError(
            "Too many registration attempts. Please try again later."
        )

    if existing_user:
        if is_unverified_user_expired(existing_user):
            existing_user.delete()

            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                is_verified=False,
                is_active=True,
            )
        else:
            existing_user.full_name = full_name
            existing_user.set_password(password)
            existing_user.save(update_fields=["full_name", "password"])
            user = existing_user
    else:
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            is_verified=False,
            is_active=True,
        )

    code = generate_verification_code()

    print("===================================")
    print(f"VERIFY CODE for {email}: {code}")
    print("===================================")

    save_email_verification_code(email, code)
    set_register_cooldown(email)
    increment_register_count(email)

    return user


def verify_email(data: dict) -> User:
    email = normalize_email(data["email"])
    code = data["code"].strip()

    user = User.objects.filter(email=email).first()

    if not user:
        raise UserNotFoundError(
            "User with this email was not found."
        )

    if user.is_verified:
        raise UserAlreadyVerifiedError(
            "User is already verified."
        )

    stored_code = get_email_verification_code(email)
    if stored_code is None:
        raise VerificationCodeExpiredError(
            "Verification code not found or expired."
        )

    if stored_code != code:
        raise InvalidVerificationCodeError(
            "Invalid verification code."
        )

    with transaction.atomic():
        user.is_verified = True
        user.save(update_fields=["is_verified"])

    delete_email_verification_code(email)
    return user


def resend_verification_code(email: str) -> None:
    email = normalize_email(email)
    user = User.objects.filter(email = email).first()

    if not user:
        raise UserNotFoundError(
            "User with this email was not found."
        )

    if user.is_verified:
        raise UserAlreadyVerifiedError(
            "User is already verified."
        )

    if has_resend_cooldown(email):
        raise ResendCooldownError(
            "Please wait before requesting another verification code."
        )

    if has_expeered_resend_limit(email):
        raise ResendLimitExceededError(
            "Too many resend attempts. Please try again later."
        )
    code = generate_verification_code()
    save_email_verification_code(email, code)
    set_resend_cooldown(email)
    increment_resend_count(email)

    print("===================================")
    print(f"RESEND VERIFY CODE for {email}: {code}")
    print("===================================")

def get_resend_cooldown_key(email: str) -> str:
        return f"resend_cooldown:{normalize_email(email)}"

def has_resend_cooldown(email: str) -> bool:
    key = get_resend_cooldown_key(email)
    return redis_client.exists(key) == 1

def set_resend_cooldown(email: str) -> None:
    key = get_resend_cooldown_key(email)
    redis_client.setex(key, RESEND_COOLDOWN_TTL, "1")

def get_resend_count_key(email: str) -> str:
    return f"resend_count:{normalize_email(email)}"

def get_resend_count(email: str) -> int:
    key = get_resend_count_key(email)
    value = redis_client.get(key)

    if value is None:
        return 0
    return int(value)

def has_expeered_resend_limit(email: str) -> bool:
    return get_resend_count(email) >= RESEND_MAX_COUNT

def increment_resend_count(email: str) -> int:
    key = get_resend_count_key(email)

    if redis_client.exists(key):
        redis_client.incr(key)
    else:
        redis_client.setex(key, RESEND_LIMIT_WINDOW, "1")


