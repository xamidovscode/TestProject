from rest_framework import serializers
from .models import Post
from apps.comments.models import Comment

class PostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'title',
            'content'
        )


class PostCommentListSerializer(serializers.ModelSerializer):
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
    comments_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "comments_count",
            "is_liked",
            "like_count",
            "created_at",
            "updated_at",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    comments = CommentListSerializer(read_only=True, many=True)
    comments_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "comments_count",
            "comments",
            "is_liked",
            "like_count",
            "created_at",
            "updated_at"
        )


class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "title", "content"
        )


