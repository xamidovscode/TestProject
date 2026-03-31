from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(
        min_length=2, max_length=100,
        write_only=True, required=False
    )
    password = serializers.CharField(
        write_only=True, min_length=8, required=True
    )

    def validate(self, attrs):
        email = attrs['email']

        user = User.objects.filter(email=email, is_verified=True).first()

        if user:
            raise serializers.ValidationError({
                'email': 'Bunday email allaqachon ro\'yhatdan o\'tgan!',
            })

        return attrs




class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.strip().lower()

    def to_service_data(self)->dict:
        return self.validated_data
