from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from utils.permissions import IsVerifiedUser, IsCommentOwner
from drf_spectacular.utils import extend_schema_view,extend_schema
from apps.posts.models import Post
from .models import Comment
from .serializers import (
    CommentListSerializer,
    CommentWriteSerializer,
    CommentUpdateSerializer,
    CommentDetailSerializer
)

@extend_schema_view(
    get=extend_schema(tags=["Comments"]),
    post=extend_schema(tags=["Comments"]),
)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.none()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Comment.objects.none()

        return Comment.objects.select_related("author", "post").filter(
            post=self.kwargs["pk"]
        ).order_by("-created_at")

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return (IsAuthenticated(), IsVerifiedUser())

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        return CommentWriteSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        serializer.save(
            author=self.request.user,
            post=post
        )

@extend_schema_view(
    get=extend_schema(tags=["Comments"]),
    put=extend_schema(tags=["Comments"]),
    patch=extend_schema(tags=["Comments"]),
    delete=extend_schema(tags=["Comments"]),
)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related('author', 'post').all()
    permission_classes = (IsCommentOwner,)
    lookup_url_kwarg = 'comment_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentDetailSerializer
        return CommentUpdateSerializer

