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
    pagination_class = PostPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PostFilter

    search_fields = ('author__full_name','title')
    ordering_fields = ('title', 'created_at', 'updated_at')



    def get_queryset(self):
        queryset = Post.objects.select_related('author').all().order_by('-created_at')
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostWriteSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsVerifiedUser()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('author').all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "Post muvaffaqiyatli o‘chirildi"
        },status=status.HTTP_204_NO_CONTENT)










