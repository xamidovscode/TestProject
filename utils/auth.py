import random


def generate_auth_code():
    # return str(random.randint(1000, 9999))
    return "7777"


def send_verify_code(email, code):
    return True







# class RegisterAPIView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         data = serializer.validated_data
#         email = data['email']
#
#         if self.get_code_from_cache(email):
#             raise ValidationError({
#                 "email": "Sizga allaqachon tasdiqlash kodi yuborilgan!"
#             })
#
#         user = User.objects.filter(email=email, is_verified=False).first()
#
#         if user:
#             user.full_name = data['full_name']
#             user.password = data['password']
#             user.save()
#
#         if not user:
#             user = User.objects.create_user(email=email, password=data['password'], full_name=data['full_name'])
#
#         code = generate_auth_code()
#         send_verify_code(email, code)
#         self.save_code_to_cache(email, code)
#         return Response({"success": True})
#
#     @staticmethod
#     def save_code_to_cache(email, code):
#         key = f"verify_email:{email}"
#         cache.set(key, code, timeout=120)
#
#     @staticmethod
#     def get_code_from_cache(email):
#         return cache.get(f"verify_email:{email}")
#
#
# class VerifyEmailAPIView(generics.GenericAPIView):
#     serializer_class = VerifyEmailSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data
#
#         email = validated_data['email']
#         code = validated_data['code']
#
#         code_from_cache = self.get_code_from_cache(email)
#
#         if not code_from_cache:
#             raise ValidationError({
#                 'code': "Kod eskirgan qayta ro\'yhatdan o\'ting!"})
#
#         if code_from_cache != code:
#             raise ValidationError({
#                 "code": "Xato kod kiritildi!"
#             })
#
#         user = User.objects.filter(email=email).first()
#
#         if user.is_verified:
#             raise ValidationError({
#                 "code": "Allaqschon tasdiqlandi tizimga kiring!!"
#             })
#
#         user.is_verified = True
#         user.save()
#
#         return Response(
#             {"message": "Email verified successfully."},
#             status=status.HTTP_200_OK
#         )
#
#     @staticmethod
#     def get_code_from_cache(email):
#         key = f"verify_email:{email}"
#         return cache.get(key)
#


# class VerifyEmailAPIView(generics.GenericAPIView):
#     serializer_class = VerifyEmailSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.to_service_data()
#
#         try:
#             user = verify_email(data)
#         except UserNotFoundError as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except UserAlreadyVerifiedError as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except VerificationCodeExpiredError as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except InvalidVerificationCodeError as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         return Response(
#             {
#                 "message": "Email verified successfully.",
#                 "email": user.email,
#                 "is_verified": user.is_verified,
#             },
#             status=status.HTTP_200_OK
#         )


