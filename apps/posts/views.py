from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.common.permissions import IsOwnerOrReadOnly, IsVerifiedUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from utils.filters import PostFilter
from utils.pagination import PostPagination
from .models import Post

from .serializers import (
    PostWriteSerializer,
    PostListSerializer,
    PostUpdateSerializer,
    PostDetailSerializer)

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related('author').order_by('-created_at')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('author__full_name','title')
    pagination_class = PostPagination
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostWriteSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(), )
        return IsAuthenticated(), IsVerifiedUser()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('author')
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer




