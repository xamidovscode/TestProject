from datetime import datetime

from django.db.models import Q
from rest_framework import generics, status, response
from rest_framework.permissions import IsAuthenticated,AllowAny

from .permissions import IsVerifiedUser,IsOwnerOrReadOnly
from rest_framework.response import Response
from .pagination import PostPagination
from .models import Post

from .serializers import (
    PostWriteSerializer,
    PostListSerializer,
    PostUpdateSerializer,
    PostDetailSerializer)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer
    permission_classes = (IsAuthenticated,IsVerifiedUser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (AllowAny,)
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.select_related('author').all().order_by('-created_at')

        search = self.request.query_params.get('search')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if search:
            search = search.strip()
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__gte=date_from)
            except ValueError:
                pass

        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__lte=date_to)
            except ValueError:
                pass

        return queryset


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










