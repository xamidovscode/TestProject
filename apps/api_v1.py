from django.urls import path, include


urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('', include('apps.posts.urls')),
]