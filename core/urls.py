from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard page
    path('', views.home_view, name='home'),  # Home page
]