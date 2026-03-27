from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(min_length=2, max_length=100)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
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


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6,max_length=10)

    def validate_email(self, value):
        return value.strip().lower()

    def validate_code(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Validation code is required.")
        return value

    def to_service_data(self)->dict:
        return self.validated_data
