# post/urls.py

from django.urls import path
from .views import post_list_view, post_detail_view, add_post_view

urlpatterns = [
    path('', post_list_view, name='post_list'),  # List view of posts
    path('<int:pk>/', post_detail_view, name='post_detail'),  # Detail view for a specific post
    path('add/', add_post_view, name='add_post'),  # Detail view for a specific post
    
]
