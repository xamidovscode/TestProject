from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .services.services import save_pending_registration
from .serializers import VerifyEmailSerializer
from .services.services import (
    verify_email_registration,
    PendingRegistrationExpiredError,
    VerificationCodeExpiredError,
    InvalidVerificationCodeError,
    UserAlreadyExistsError,
)

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        save_pending_registration(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )

        return Response(
            {
                "message": "Registration data saved successfully. Please complete verification."
            },
            status=status.HTTP_201_CREATED,
        )

class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.to_service_data()

        try:
            user = verify_email_registration(data)
        except PendingRegistrationExpiredError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except VerificationCodeExpiredError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidVerificationCodeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except UserAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        return Response(
            {
                "message": "Email verified successfully",
                "user_id": str(user.id),
            },
            status=status.HTTP_201_CREATED,
        )