import re

from django.db import transaction
from rest_framework import serializers

from .models import User, EmailVerificationToken


USERNAME_REGEX = r"^[a-zA-Z0-9_]+$"


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=32)
    full_name = serializers.CharField(min_length=2, max_length=100)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate_username(self, value):
        value = value.strip()

        if not re.fullmatch(USERNAME_REGEX, value):
            raise serializers.ValidationError(
                "Username may contain only letters, numbers, and underscores."
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate_full_name(self, value):
        value = value.strip()

        if len(value) < 2 or len(value) > 100:
            raise serializers.ValidationError(
                "Full name must be between 2 and 100 characters."
            )

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        if value.isdigit():
            raise serializers.ValidationError(
                "Password cannot be entirely numeric."
            )

        return value

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            verification_token = EmailVerificationToken.create_for_user(user)

        user.verification_token = verification_token.token
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email').strip().lower()
        token = attrs.get('token').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                'email':'User with this email does not exist.'
                }
            )

        verification_token = (
            EmailVerificationToken.objects.
            filter(
                user=user,
                token=token,
                is_used=False
            )
            .order_by('-created_at')
            .first()
        )

        if not verification_token:
            raise serializers.ValidationError(
                {
                    'token':'Invalid or already used token.',
                }
            )

        attrs['user'] = user
        attrs['verification_token'] = verification_token
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        verification_token = self.validated_data['verification_token']

        user.is_verified = True
        user.save(update_fields=['is_verified'])

        verification_token.is_used = True
        verification_token.save(update_fields=['is_used'])
        return user