from  django.urls import path
from rest_framework.views import APIView

from .import views

urlpatterns = [
    path('register/',views.RegisterAPIView.as_view(),name='register'),
    path('verify-email/',views.ValidateEmailAPIView.as_view(),name='verify_email'),
    path('resend-code/',views.ResendCodeAPIView.as_view(),name='resend_code'),
    path('login/',views.LoginAPIView.as_view(),name='login'),
]

