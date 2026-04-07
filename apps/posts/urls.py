from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostCreateAPIView.as_view(), name="post-create"),
    path("posts-list/",views.PostListAPIView.as_view(), name="post-list"),
    path("post-detail/<uuid:pk>/",views.PostDetailAPIView.as_view(), name="post-detail"),
]