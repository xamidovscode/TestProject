from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, models


class LoginAPIView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = user.get_tokens_for_user()

        return Response(
            {
                "user_id": user.id,
                "username": user.username,
                'full_name': user.full_name,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            },
            status=status.HTTP_200_OK
        )


class ProfileAPIView(generics.GenericAPIView):

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({
            "id": instance.id,
            "username": instance.username,
            "full_name": instance.full_name,
        })


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by("-id")
    serializer_class = serializers.RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by("-id")
    serializer_class = serializers.UserSerializer
