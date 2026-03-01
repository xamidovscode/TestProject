from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('profile/', views.ProfileAPIView.as_view(), name='login'),
]

