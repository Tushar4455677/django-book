from django.contrib import admin  # Admin site module
from django.urls import path, include  # For defining URL patterns and including app-specific URLs
from django.conf import settings  # To access project settings
from django.conf.urls.static import static  # To serve media files during development
from django.shortcuts import redirect  # To handle URL redirection
from users.views import about_view, contact_view  # Importing views for about and contact pages
from movies import views  # Importing views from the movies app

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin dashboard URL
    path('users/', include('users.urls')),  # Include URL patterns from users app
    path('movies/', include('movies.urls')),  # Include URL patterns from movies app
    path('about/', about_view, name='about'),  # About page URL
    path('contact/', contact_view, name='contact'),  # Contact page URL
    path('recommended/', views.recommended_movies, name='recommended_movies'),  # URL for recommended movies

    #  Redirect root path "/" to the movie list view
    path('', lambda request: redirect('movie_list')),  # Redirect root URL to movie list
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve uploaded media files
