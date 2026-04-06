from rest_framework import serializers

from utils import auth
from .models import Post
from .. import users


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content'
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "title bo'sh bo'lishi mumkin emas"
            )

        if not (5 <= len(value) <= 255):
            raise serializers.ValidationError(
                "Sarlavha 5 dan 255 tagacha belgidan iborat bo'lishi kerak"
            )
        return value

    def validate_content(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "content bo'sh bo'lishi mumkin emas"
            )

        if len(value) > 10000:
            raise serializers.ValidationError(
                "Kontent 10000 belgidan oshmasligi kerak"
            )
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        title = attrs.get('title')
        content = attrs.get('content')

        if Post.objects.filter(
                author=user,
                title=title,
                content=content
        ).exists():
            raise serializers.ValidationError("Bunday post allaqachon mavjud")

        return attrs


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author_id",
            "title",
            "content",
            "created_at",
        ]