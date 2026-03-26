from  django.urls import path
from .import views

urlpatterns = [
    path('auth/register/',views.RegisterAPIView.as_view(),name='register'),
    path('auth/verify-email/',views.VerifyEmailAPIView.as_view(),name='verify_email'),
]