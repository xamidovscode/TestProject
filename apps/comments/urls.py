from django.urls import path
from . import views

urlpatterns = [
    path('posts/<uuid:pk>/comments/', views.CommentListCreateAPIView.as_view(), name='comments'),
    path('posts/<uuid:pk>/comments/<uuid:comment_id>/', views.CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment'),

]