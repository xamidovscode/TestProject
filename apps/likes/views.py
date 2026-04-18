from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view,extend_schema

from apps.likes.models import Like
from apps.posts.models import Post
from apps.likes.serializers import EmptySerializer


@extend_schema_view(
    post=extend_schema(tags=["Like"]),
    delete=extend_schema(tags=["Like"]),
)

class LikeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmptySerializer

    def get_post(self):
        return get_object_or_404(
            Post.objects.select_related('author'),
            pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        post = self.get_post()

        if post.author == request.user:
            return Response(
                {"message": "O'zingizning postingizga like bosa olmaysiz."},
                status=status.HTTP_400_BAD_REQUEST
            )

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            return Response(
                {
                    "message": "Siz bu postga allaqachon like bosgansiz.",
                    "liked": True,
                    "like_count": post.likes.count()
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Like muvaffaqiyatli qo'yildi.",
                "liked": True,
                "like_count": post.likes.count()
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_post()

        like = Like.objects.filter(
            user=request.user,
            post=post
        ).first()

        if not like:
            return Response(
                {
                    "message": "Like topilmadi.",
                    "liked": False,
                    "like_count": post.likes.count()
                },
                status=status.HTTP_404_NOT_FOUND
            )

        like.delete()

        return Response(
            {
                "message": "Like olib tashlandi.",
                "liked": False,
                "like_count": post.likes.count()
            },
            status=status.HTTP_200_OK
        )