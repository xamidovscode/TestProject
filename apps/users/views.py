import email

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from utils.auth import generate_auth_code, send_verify_code
from django.core.cache import cache
from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    ResendCodeSerializer, LoginSerializer, ForgotPasswordSerializer
)
User = get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        if self.get_code_from_cache(email):
            raise ValidationError({
                "message": "Sizga allaqachon kod yuborilgan!"
            })

        verified_user = User.objects.filter(email=email, is_verified=True).first()
        if verified_user:
            raise ValidationError({
                "message": "Bu email bilan user allaqachon ro'yhatdan o'tgan!"
            })

        user = User.objects.filter(email=email, is_verified=False).first()
        if user:
            user.full_name = validated_data['full_name']
            user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                email=email,
                full_name=validated_data['full_name'],
                password=validated_data['password'],
                is_verified=False
            )
        code = generate_auth_code()
        send_verify_code(email, code)
        self.save_code_to_cache(email, code)
        return Response(
            {
                "success": True,
            }
        )

    @staticmethod
    def save_code_to_cache(email,code):
        key = f"verify_code:{email}"
        cache.set(key, code, timeout=120)

    @staticmethod
    def get_code_from_cache(email):
        key = f"verify_code:{email}"
        return cache.get(key)

class ValidateEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        code = validated_data['code']

        code_from_cache = self.get_code_from_cache(email)

        if not code_from_cache:
            raise ValidationError({
                "message": "Kod eskirgan, qayta kod yuborish ni bosing."
            })

        if code != code_from_cache:
            raise ValidationError({
                    "Xato kod kiritildi."
                })

        user = User.objects.filter(email=email).first()

        if user.is_verified:
            raise ValidationError({
                "Allaqachon tasdiqlangan, tizimga kiring."
            })

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        self.delete_code_from_cache(email)

        return Response(
            {
                "message": "Email muvafaqiyatlik tasdiqlandi"
            },
            status=status.HTTP_200_OK
        )

    @staticmethod
    def get_code_from_cache(email):
        key = f"verify_code:{email}"
        return cache.get(key)

    @staticmethod
    def delete_code_from_cache(email):
        key = f"verify_code:{email}"
        cache.delete(key)


class ResendCodeAPIView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']

        code_from_cache = self.get_code_from_cache(email)

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({
                "message": "Siz ro'yhatdan o'tmagansiz, iltimos ro'yhatdan o'ting."
            })

        if user.is_verified:
            raise ValidationError({
                "message": "Allaqachon tasdiqlangan, tizimga kiring."
            })

        if code_from_cache:
            raise ValidationError({
                "message": "Kod allaqachon yuborilgan, biroz kuting"
            })

        code = generate_auth_code()
        send_verify_code(email, code)
        self.save_code_to_cache(email, code)
        return Response({"success": True}, status=status.HTTP_200_OK)

    @staticmethod
    def save_code_to_cache(email, code):
        key = f"verify_code:{email}"
        cache.set(key, code, timeout=120)

    @staticmethod
    def get_code_from_cache(email):
        key = f"verify_code:{email}"
        return cache.get(key)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({
                "message": "User topilmadi!"
            })

        if not user.is_verified:
            raise ValidationError({
                "message": "Tizimga kirish uchun, Emailni tasdiqlang!"
            })

        if not user.check_password(password):
            raise ValidationError({
                "message": "Email yoki parol xato!"
            })

        return  Response(user.get_tokens(), status=status.HTTP_200_OK)










