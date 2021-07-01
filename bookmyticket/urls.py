from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome),
    path('movies/', views.movies),
    path('cinemas/', views.cinema),
    path('showtimes/', views.showtimes),
    path('ongoing_shows', views.ongoing_shows),
    path('booking/', views.booking),
    path('get_shows/', views.getshows),
    path('get_cinemas/', views.get_cinemas),
    path('register/', views.register_user),
]