from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListCreateAPIView.as_view(), name="post-list-create"),
    path("posts/<uuid:pk>/",views.PostDetailAPIView.as_view(), name="post-detail"),
]