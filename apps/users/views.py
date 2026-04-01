from wsgiref import validate

from asgiref import timeout
from django.db.migrations import serializer
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from yaml import serialize_all

from utils.auth import generate_auth_code, send_verify_code
from django.core.cache import cache
from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    ResendCodeSerializer
    )
from .services.services import (
    register_user,
    verify_email,
    resend_verification_code,

    UserNotFoundError,
    UserAlreadyVerifiedError,
    UserAlreadyExistsError,
    VerificationCodeExpiredError,
    InvalidVerificationCodeError,

    RegisterCooldownError,
    RegisterLimitExceededError,

    ResendCooldownError,
    ResendLimitExceededError, User, save_email_verification_code
    )
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']

        if self.get_code_from_cach(email):
            raise   ValidationError("Kod allaqachon yuborilgan")

        user = User.objects.filter(email=email, is_verified=False).first()

        if user:
            user.full_name = validated_data['full_name']
            user.password = validated_data['password']
            user.save()

        if not user:
            user = User.objects.filter(
                email=email,
                full_name=validated_data['full_name'],
                password=validated_data['password']
            )

        code = generate_auth_code()
        send_verify_code(email, code)
        self.save_code_to_cach(email, code)
        return Response({"success": True})


    @staticmethod
    def save_code_to_cach(email,code):
        key = f"verify_{email}"
        cache.set(key, code, timeout=120)

    @staticmethod
    def get_code_from_cach(email,code):
        return code.get(f"verify_email: {email}")

class VerifyEmailAPIView(generics.RetrieveAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        code = validated_data['code']

        code_from_cache = self.get_code_from_cach(email, code)

        if not code_from_cache:
            raise ValidationError("Kod eskirgan qaytadan ro'hatdan o'ting.")

        if code != code_from_cache:
            raise ValidationError("Xato kod kiritildi.")

        user = User.objects.filter(email=email).first()

        if user.is_verified:
            raise ValidationError("Allaqachon tasdiqlangan tizimga kiring.")

        user.is_verified = True
        user.save()
        return Response({"success": True})

    @staticmethod
    def get_code_from_cach(email):
        key = f"verify_{email}"
        return cache.get(key)

