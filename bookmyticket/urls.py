from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome),
    path('movies/', views.movies),
    path('cinemas/', views.cinema),
    path('showtimes/', views.showtimes),
    path('shows', views.ongoing_shows),
]