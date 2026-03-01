from django.contrib.auth import authenticate
from rest_framework import serializers

from utils.exceptions import BadRequest
from . import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise BadRequest({
                "msg": "Username va password majburiy"
            })

        user = authenticate(username=username, password=password)

        if not user:
            raise BadRequest({
                "msg": "Login yoki parol noto‘g‘ri"
            })

        if not user.is_active:
            raise BadRequest({
                "msg": "User aktiv emas"
            })

        attrs["user"] = user
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
