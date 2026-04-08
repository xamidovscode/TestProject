from rest_framework import serializers
from .models import Comment


class CommentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'comment')
        read_only_fields = ('id',)


class CommentListSerializer(serializers.ModelSerializer):
    author_id = serializers.UUIDField(source="author.id", read_only=True)
    post_id = serializers.UUIDField(source="post.id", read_only=True)
    author_name = serializers.CharField(source="author.full_name", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            'author_id',
            'post_id',
            'author_name',
            'comment',
            'created_at',
            'updated_at'
        ]

class CommentDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_id = serializers.UUIDField(source="author.id", read_only=True)
    post_id = serializers.UUIDField(source="post.id", read_only=True)

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


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment',)