from  django.urls import path
from rest_framework.views import APIView

from .import views

urlpatterns = [
    path('auth/register/',views.RegisterAPIView.as_view(),name='register'),
    path('auth/verify-email/',views.ValidateEmailAPIView.as_view(),name='verify_email'),
    path('auth/resend-code/',views.ResendCodeAPIView.as_view(),name='resend_code'),
    path('auth/login/',views.LoginAPIView.as_view(),name='login'),
]

