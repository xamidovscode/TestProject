from django.urls import path

from . import views

urlpatterns = [
    # users
    path("users/", views.UserViewSet.as_view({"get": "list", "post": "create"})),
    path("users/<int:pk>/", views.UserViewSet.as_view({"delete": "destroy", "patch": "partial_update"})),

    # roles
    path("roles/", views.RoleViewSet.as_view({"get": "list", "post": "create"})),
    path("roles/<int:pk>/", views.RoleViewSet.as_view({"delete": "destroy", "patch": "partial_update"})),

    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('profile/', views.ProfileAPIView.as_view(), name='login'),
]
