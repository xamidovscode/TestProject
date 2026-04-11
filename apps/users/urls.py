from  django.urls import path
from .import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('verify-email/', views.VerifyEmailAPIView.as_view(), name='verify_email'),
    path('resend-code/', views.ResendCodeAPIView.as_view(), name='resend_code'),
    path('login/', views.LoginAPIView.as_view(), name='login'),

    path('forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-verify/', views.VerifyResetCodeAPIView.as_view(), name='reset_verify_email'),
    path('resend-reset-code/',views.ResendResetCodeAPIView.as_view(), name='resend_reset_code'),
    path('reset-password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),

    path('get-me/', views.GetMeAPIView.as_view(), name='get_me'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]

