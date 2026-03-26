from pyexpat.errors import messages
from threading import gettrace

from  rest_framework import  generics, status
from  rest_framework.response import Response
from .serializers import RegisterSerializer, VerifyEmailSerializer
from django.conf import settings

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
                "messages":"User registered successfully",
                'user':{
                    'id':user.id,
                    'email':user.email,
                    'username':user.username,
                    'full_name':user.full_name,
                    'is_verified':user.is_verified,
                    'created_at':user.created_at,
                },
            }
        if settings.DEBUG:
            response_data["verification_token"] = getattr(
                user,
                "verification_token", None)
            return Response(response_data, status=status.HTTP_201_CREATED)

class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        return Response(
            {
                "messages":"Email verified successfully",
                'user':{
                    'id':str(user.id),
                    'email':user.email,
                    'is_verified':user.is_verified,
                }
        },
            status=status.HTTP_200_OK
        )
