from django.contrib import admin  # Importing Django admin module
from .models import Movie, Theater, Seat, Booking, Genre, Language  # Importing models to register in admin panel

# Registering Movie model with custom admin configuration
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # Fields to display in the Movie list view in admin
    list_display = ['name', 'rating', 'cast', 'description', 'release_date', 'get_languages', 'get_genres']
    
    # Enables a horizontal filter widget for many-to-many relationship (genre)
    filter_horizontal = ['genre']

    # Custom method to display comma-separated genres
    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genre.all()])
    get_genres.short_description = 'Genres'  # Column header in admin panel

    # Custom method to display language name
    def get_languages(self, obj):
        return obj.language.name if obj.language else '-'
    get_languages.short_description = 'Language'  # Column header in admin panel

# Registering Theater model with admin configuration
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    # Fields to display in the Theater list view
    list_display = ['name', 'movie', 'time']

# Registering Seat model with admin configuration
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    # Fields to display in the Seat list view
    list_display = ['theater', 'seat_number', 'is_booked']

# Registering Booking model with admin configuration
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Fields to display in the Booking list view
    list_display = ['user', 'seat', 'movie', 'theater', 'booked_at']

# Registering Genre model with admin configuration
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Field to display in the Genre list view
    list_display = ['name']

# Registering Language model with admin configuration
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    # Field to display in the Language list view
    list_display = ['name']
