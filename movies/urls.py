from django.urls import path  # Importing path for defining URL patterns
from . import views  # Importing views from the current app

urlpatterns = [
    path('', views.movie_list, name='movie_list'),  # URL for listing all movies
    path('<int:movie_id>/theaters/', views.theater_list, name='theater_list'),  # URL for listing theaters for a specific movie
    path('theater/<int:theater_id>/seats/', views.book_seats, name='book_seats'),  # URL for booking seats in a specific theater
    path('', views.movie_list, name='movies'),  # Duplicate root URL pattern for movie list (may cause conflicts)
]
