from rest_framework import  generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.common.permissions import IsVerifiedUser, IsCommentOwner
from apps.posts.models import Post
from .models import Comment
from .serializers import (
    CommentListSerializer,
    CommentWriteSerializer,
    CommentUpdateSerializer,
    CommentDetailSerializer
)


class CommentListCreateAPIView(generics.ListCreateAPIView):

    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'post').filter(
            post_id=self.kwargs['pk']
        ).order_by('-created_at')
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsVerifiedUser()]

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


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related('author', 'post').all()
    permission_classes = [IsCommentOwner]
    lookup_url_kwarg = 'comment_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentDetailSerializer
        return CommentUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)


        return Response({
           "message": "Comment muvaffaqiyatli o‘chirildi"
        }, status=status.HTTP_204_NO_CONTENT)
