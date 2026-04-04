from  django.urls import path
from rest_framework.views import APIView

from .import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('verify-email/', views.ValidateEmailAPIView.as_view(), name='verify_email'),
    path('resend-code/', views.ResendCodeAPIView.as_view(), name='resend_code'),
    path('login/', views.LoginAPIView.as_view(), name='login'),

    path('forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-verify/', views.VerifyResetCodeAPIView.as_view(), name='reset_verify_email'),
    path('reset-password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),

    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]

