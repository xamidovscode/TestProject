from rest_framework import serializers
from .models import Post

class PostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content'
        )


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "created_at",
            "updated_at",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "created_at",
            "updated_at"
        )

class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "title", "content"
        )


