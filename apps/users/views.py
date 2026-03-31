from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    ResendCodeSerializer
)
from .services.services import (
    register_user,
    verify_email,
    resend_verification_code,

    UserNotFoundError,
    UserAlreadyVerifiedError,
    UserAlreadyExistsError,
    VerificationCodeExpiredError,
    InvalidVerificationCodeError,

    RegisterCooldownError,
    RegisterLimitExceededError,

    ResendCooldownError,
    ResendLimitExceededError
)

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.to_service_data()
        try:
            user = register_user(data)

        except UserAlreadyExistsError as e:
            return Response(
            {"detail": str(e)},
                status=status.HTTP_409_CONFLICT
            )

        except RegisterCooldownError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        except RegisterLimitExceededError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return Response(
            {
                "message": "Registration successful. Verification code has been generated.",
                "email": user.email,
                "is_verified": user.is_verified,
            }
        )

class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.to_service_data()

        try:
            user = verify_email(data)
        except UserNotFoundError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except UserAlreadyVerifiedError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except VerificationCodeExpiredError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidVerificationCodeError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Email verified successfully.",
                "email": user.email,
                "is_verified": user.is_verified,
            },
            status=status.HTTP_200_OK
        )

class ResendCodeAPIView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.to_service_data()
        resend_verification_code(**data)

        try:
            resend_verification_code(**data)
        except UserNotFoundError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        except UserAlreadyVerifiedError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except ResendCooldownError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        except ResendLimitExceededError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return Response(
            {
                "message": "Verification code sent.",
            },
            status=status.HTTP_200_OK
        )
