from django.urls import path
from . import views

urlpatterns = [
    path('posts/<uuid:pk>/like/', views.LikeAPIView.as_view(), name='like_post'),
]