from django.shortcuts import render

from  rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsVerifiedUser
from rest_framework.response import Response

from .models import Post
from .serializers import PostWriteSerializer,PostListSerializer

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostWriteSerializer
    permission_classes = (IsAuthenticated,IsVerifiedUser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostListSerializer
    permission_classes = (AllowAny,)





