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


class CommentListSerializer(serializers.ModelSerializer):
    author_id = serializers.UUIDField(source="author.id", read_only=True)
    post_id = serializers.UUIDField(source="post.id", read_only=True)
    author_name = serializers.CharField(source="author.full_name", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            'author_id',
            'post_id',
            'author_name',
            'comment',
            'created_at',
            'updated_at'
        )


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    comments = CommentListSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "comments",
            "created_at",
            "updated_at",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    comments = CommentListSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "comments",
            "created_at",
            "updated_at"
        )


class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "title", "content"
        )


