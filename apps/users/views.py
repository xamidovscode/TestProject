from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

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


class ProfileAPIView(generics.RetrieveAPIView):

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({
            "id": instance.id,
            "username": instance.username,
            "full_name": instance.full_name,
        })

