from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from utils.auth import BrevoEmailError, send_verify_code,generate_auth_code
from django.core.cache import cache
from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    ResendCodeSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResendResetCodeSerializer,
    VerifyResetCodeSerializer,
    ResetPasswordSerializer,
    LogoutSerializer,
    GetMeSerializer
)
from apps.users.models import User


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        count = self.get_sms_count(email)

        if count >= 5:

            raise ValidationError({
                "message": "Juda ko'p urinish, keyinroq qayta urinib ko'ring"
            })

        if self.get_code_from_cache(email):
            raise ValidationError({
                "message": "Sizga allaqachon kod yuborilgan!"
            })

        existing_user = User.objects.filter(email=email).order_by('-created_at').first()

        if existing_user and existing_user.is_verified:
            raise ValidationError({
                "message": "Bu email bilan user allaqachon ro'yhatdan o'tgan!"
            })

        if existing_user and not existing_user.is_verified:
            existing_user.full_name = validated_data['full_name']
            existing_user.set_password(password)
            existing_user.save()
        else:
            User.objects.create_user(
                email=email,
                full_name=validated_data['full_name'],
                password=validated_data['password'],
                is_verified=False
            )
        code = generate_auth_code()

        try:
            send_verify_code(email, code)
        except BrevoEmailError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            return Response(
                {"success": False, "message": "Kod emailga yuborilmadi."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.save_code_to_cache(email, code)
        self.increment_sms_count(email)
        return Response(
            {
            "success": True,
        }
        )

    @staticmethod
    def save_code_to_cache(email,code):
        key = f"verify_code:{email}"
        cache.set(key, code, timeout=120)

    @staticmethod
    def get_code_from_cache(email):
        key = f"verify_code:{email}"
        return cache.get(key)

    @staticmethod
    def get_sms_count(email):
        key = f"sms_count:{email}"
        count = cache.get(key)

        if count is None:
            return 0

        return count

    @staticmethod
    def increment_sms_count(email):
        key = f"sms_count:{email}"
        count = cache.get(key)

        if count is None:
            cache.set(key, 1, timeout=43200)
        else:
            cache.set(key, count + 1, timeout=43200)


class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        code = validated_data['code']

        code_from_cache = self.get_code_from_cache(email)
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({
                "message": "User topilmadi"
            })

        if user.is_verified:
            raise ValidationError({
                "message": "Allaqachon tasdiqlangan, tizimga kiring."
            })

        if not code_from_cache:
            raise ValidationError({
                "message": "Kod eskirgan, qayta kod yuborish ni bosing."
            })

        if code != code_from_cache:
            self.increment_count_attempts(email)
            count = self.get_attempts_count(email)

            if count >= 3:
                self.clear_verify_attempts(email)
                self.delete_code_from_cache(email)
                raise ValidationError({
                    "message": "Juda ko'p xato urinish. Yangi kod so'rang"
                })

            raise ValidationError({
                "message": "Xato kod kiritildi"
            })

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        self.delete_code_from_cache(email)
        self.clear_verify_attempts(email)

        return Response(
            {
                "message": "Email muvafaqiyatlik tasdiqlandi"
            },
            status=status.HTTP_200_OK
        )

    @staticmethod
    def get_code_from_cache(email):
        key = f"verify_code:{email}"
        return cache.get(key)

    @staticmethod
    def delete_code_from_cache(email):
        key = f"verify_code:{email}"
        cache.delete(key)

    @staticmethod
    def increment_count_attempts(email):
        key = f"verify_attempts:{email}"
        count = cache.get(key)

        if count is None:
            cache.set(key, 1, 120)
        else:
            cache.set(key, count + 1, 120)

    @staticmethod
    def get_attempts_count(email):
        key = f"verify_attempts:{email}"
        count = cache.get(key)

        if count is None:
            return 0
        return count

    @staticmethod
    def clear_verify_attempts(email):
        key = f"verify_attempts:{email}"
        cache.delete(key)


class GetMeAPIView(generics.RetrieveAPIView):
    serializer_class = GetMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ResendCodeAPIView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']

        count = self.get_sms_code(email)

        if count >= 5:
            raise ValidationError({
                "message": "Juda ko'p urinish, keyinroq qayta urinib ko'ring!"
            })

        code_from_cache = self.get_code_from_cache(email)

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({
                "message": "Siz ro'yhatdan o'tmagansiz, iltimos ro'yhatdan o'ting."
            })

        if user.is_verified:
            raise ValidationError({
                "message": "Allaqachon tasdiqlangan, tizimga kiring."
            })

        if code_from_cache:
            raise ValidationError({
                "message": "Kod allaqachon yuborilgan, biroz kuting"
            })

        code = generate_auth_code()

        try:
            send_verify_code(email, code)
        except BrevoEmailError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            return Response(
                {"success": False, "message": "Kod emailga yuborilmadi."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.save_code_to_cache(email, code)
        self.increment_sms_count(email)
        return Response({"success": True}, status=status.HTTP_200_OK)

    @staticmethod
    def save_code_to_cache(email, code):
        key = f"verify_code:{email}"
        cache.set(key, code, timeout=120)

    @staticmethod
    def get_code_from_cache(email):
        key = f"verify_code:{email}"
        return cache.get(key)

    @staticmethod
    def get_sms_code(email):
        key = f"sms_count:{email}"
        count =  cache.get(key)

        if count is None:
            return 0

        return count

    @staticmethod
    def increment_sms_count(email):
        key = f"sms_count:{email}"
        count = cache.get(key)

        if count is None:
            cache.set(key, 1, timeout=43200)
        else:
            cache.set(key, count + 1, timeout=43200)



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({
                "message": "User topilmadi!"
            })

        if not user.is_verified:
            raise ValidationError({
                "message": "Tizimga kirish uchun, Emailni tasdiqlang!"
            })

        if not user.check_password(password):
            raise ValidationError({
                "message": "Parol xato kiritildi!"
            })

        return  Response(user.get_tokens(), status=status.HTTP_200_OK)



class ForgotPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']

        count = self.get_sms_code(email)

        if count >= 5:
            raise ValidationError({
                "message": "Juda ko'p urinish, keyinroq qaytaday urinib ko'ring"
            })


        user = User.objects.filter(email=email, is_verified=True).first()
        code_from_cache = self.get_code_from_cache(email)

        if not user:
            raise ValidationError({
                "message": "User topilmadi!"
            })

        if code_from_cache:
            raise ValidationError({
                "message": "Kod allaqachon yuborilgan, biroz kuting"
            })

        code = generate_auth_code()

        try:
            send_verify_code(email, code)
        except BrevoEmailError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            return Response(
                {"success": False, "message": "Kod emailga yuborilmadi."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        self.save_code_to_cache(email, code)
        self.increment_sms_count(email)

        return Response(
            {
                "success": True,
                "message": "Kod yuborildi, kodni tasdiqlang!"
            },
            status=status.HTTP_200_OK)

    @staticmethod
    def save_code_to_cache(email, code):
        key = f"reset_code:{email}"
        cache.set(key, code, timeout=120)

    @staticmethod
    def get_code_from_cache(email):
        key = f"reset_code:{email}"
        return cache.get(key)

    @staticmethod
    def get_sms_code(email):
        key = f"sms_count:{email}"
        count = cache.get(key)

        if count is None:
            return 0
        return count

    @staticmethod
    def increment_sms_count(email):
        key = f"sms_count:{email}"
        count = cache.get(key)

        if count is None:
            cache.set(key, 1, timeout=43200)
        else:
            cache.set(key, count + 1, timeout=43200)


class VerifyResetCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyResetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        code = validated_data['code']

        user = User.objects.filter(email=email, is_verified=True).first()
        code_from_cache = self.get_reset_code_from_cache(email)

        if not user:
            raise ValidationError({
                "message": "User topilmadi!"
            })

        if not code_from_cache:
            raise ValidationError({
                "message": "Kod eskirgan, qaytadan yoboring"
            })

        if code != code_from_cache:
            self.increment_reset_code_count(email)
            count = self.get_attempts_count(email)

            if count >= 3:
                self.clear_attempts_count(email)
                self.delete_reset_code_from_cache(email)

                raise ValidationError({
                    "message": "Juda ko'p xato urinish, qodni qaytadan yuboring"
                })

            raise ValidationError({
                "message": "Xato kod kiritildi!"
            })

        self.save_reset_verified_to_cache(email)
        self.delete_reset_code_from_cache(email)
        self.clear_attempts_count(email)

        return Response(
            {
                "success": True,
                "message": "Kod tasdiqlandi, yangi parolni kiriting"
            },
            status=status.HTTP_200_OK)

    @staticmethod
    def save_reset_verified_to_cache(email):
        key = f"reset_verified:{email}"
        cache.set(key, True, timeout=300)

    @staticmethod
    def get_reset_code_from_cache(email):
        key = f"reset_code:{email}"
        return cache.get(key)

    @staticmethod
    def delete_reset_code_from_cache(email):
        key = f"reset_code:{email}"
        cache.delete(key)

    @staticmethod
    def increment_reset_code_count(email):
        key = f"reset_verify_attempts:{email}"
        count = cache.get(key)

        if count is None:
            cache.set(key, 1, timeout=120)
        else:
            cache.set(key, count + 1, timeout=120)

    @staticmethod
    def get_attempts_count(email):
        key = f"reset_verify_attempts:{email}"
        count = cache.get(key)

        if count is None:
            return 0
        return count

    @staticmethod
    def clear_attempts_count(email):
        key = f"reset_verify_attempts:{email}"
        cache.delete(key)


class ResendResetCodeAPIView(generics.GenericAPIView):
    serializer_class = ResendResetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']

        count = self.get_sms_code(email)

        if count >= 5:
            raise ValidationError({
                "message": "Juda ko'p urinish, keyinroq qaytadan urinib ko'ring"
            })

        user = User.objects.filter(email=email).first()
        code_from_cache = self.get_reset_code_from_cache(email)

        if not user:
            raise ValidationError({
                "message": "User topilmadi!"
            })

        if not user.is_verified:
            raise ValidationError({
                "message": "Ro'yhatdan o'tmagansiz"
            })

        if code_from_cache:
            raise ValidationError({
                "message": "Kod allaqachon yuborilgan, biroz kuting "
            })

        code = generate_auth_code()

        try:
            send_verify_code(email, code)
        except BrevoEmailError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            return Response(
                {"success": False, "message": "Kod emailga yuborilmadi."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.save_reset_code_to_cache(email, code)
        self.increment_sms_count(email)

        return Response({"success": True}, status=status.HTTP_200_OK)

    @staticmethod
    def save_reset_code_to_cache(email, code):
        key = f"reset_code:{email}"
        cache.set(key,code , timeout=120)

    @staticmethod
    def get_reset_code_from_cache(email):
        key = f"reset_code:{email}"
        return cache.get(key)

    @staticmethod
    def increment_sms_count(email):
        key = f"sms_code:{email}"
        count = cache.get(key)

        if not count:
            cache.set(key, 1, timeout=43200)
        else:
            cache.set(key, count + 1, timeout=43200)

    @staticmethod
    def get_sms_code(email):
        key = f"sms_code:{email}"
        count = cache.get(key)

        if count is None:
           return 0
        return count


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.filter(email=email, is_verified=True).first()

        if not user:
            raise ValidationError({
                "message": "User topilmadi!"
            })

        if not self.get_reset_verified_from_cache(email):
            raise ValidationError({
                "message": "Avval kodni tasdiqlang"
            })

        user.set_password(password)
        user.save(update_fields=["password"])

        self.delete_reset_code_to_cache(email)
        self.delete_reset_verified_to_cache(email)

        return Response({
            "success": True,
            "message": "Parol muvaffaqiyatli yangilandi."
        }, status=status.HTTP_200_OK)

    @staticmethod
    def get_reset_verified_from_cache(email):
        key = f"reset_verified:{email}"
        return cache.get(key)

    @staticmethod
    def delete_reset_verified_to_cache(email):
        key = f"reset_verified:{email}"
        cache.delete(key)

    @staticmethod
    def delete_reset_code_to_cache(email):
        key = f"reset_code:{email}"
        cache.delete(key)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        refresh = validated_data['refresh']

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            return Response({
                "success": False,
                "message": "Token already blacklisted or invalid"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Tizimdan muvofaqiyatli chiqildi!"
        },status=status.HTTP_200_OK)













