from django.db.models import Count, Exists, OuterRef, BooleanField, Value
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema_view,extend_schema

from apps.likes.models import Like
from utils.permissions import IsOwnerOrReadOnly, IsVerifiedUser
from utils.filters import PostFilter
from .models import Post

from .serializers import (
    PostWriteSerializer,
    PostListSerializer,
    PostUpdateSerializer,
    PostDetailSerializer)

@extend_schema_view(
    post=extend_schema("POST")
)


class PostListCreateAPIView(generics.ListCreateAPIView):
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = Post.objects.select_related('author').annotate(
            comments_count=Count("comments", distinct=True),
            like_count=Count("likes", distinct=True),
        ).order_by('-created_at')

        user = self.request.user

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_liked = Exists(
                    Like.objects.filter(
                        post=OuterRef('pk'),
                        user=user
                    ))
            )
        else:
            queryset = queryset.annotate(
                is_liked = Value(False, output_field=BooleanField())
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostWriteSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return IsAuthenticated(), IsVerifiedUser()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = (Post.objects
                    .select_related('author')
                    .prefetch_related('comments')
                    .annotate(
            comments_count=Count("comments", distinct=True),
            like_count=Count("likes", distinct=True),
        ).order_by('-created_at'))

        user = self.request.user

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_liked = Exists(
                    Like.objects.filter(
                        post=OuterRef('pk'),
                        user=user
                    )
                )
            )
        else:
            queryset = queryset.annotate(
                is_liked = Value(False, output_field=BooleanField())
            )

        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return (IsAuthenticated(), IsOwnerOrReadOnly())

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer






