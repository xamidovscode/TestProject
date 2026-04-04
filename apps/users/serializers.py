
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(
        min_length=2, max_length=100, write_only=True
    )
    password = serializers.CharField(
        write_only=True, min_length=8, required=True
    )
    confirm_password = serializers.CharField(
        write_only=True, min_length=8, required=True
    )

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        user = User.objects.filter(email=email, is_verified=True).first()

        if user:
            raise serializers.ValidationError({
                'email': "Bunday email allaqachon ro'yhatdan o'tgan!",
            })


        if password != confirm_password:
            raise serializers.ValidationError({
                "password": "Parollar mos emas",
            })

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, required=False, min_length=8
    )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResendResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, min_length=8, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({
                "password": "Parollar mos emas",
            })

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()



