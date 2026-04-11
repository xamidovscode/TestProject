from django.urls import path, include


urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('', include('apps.posts.urls')),
    path('', include('apps.comments.urls')),
    path('', include('apps.likes.urls')),
]