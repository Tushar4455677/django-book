from collections import Counter  # Importing Counter to count occurrences
from movies.models import Booking  # Importing Booking model to fetch user booking data

# Function to get user's top genres and languages based on booking history
def get_user_preferences(user):
    # Fetch bookings of the user with related movie, language and genre data
    bookings = Booking.objects.filter(user=user).select_related('movie__language').prefetch_related('movie__genre')

    # If no bookings exist, return empty preferences
    if not bookings.exists():
        return {'genre_ids': [], 'language_ids': []}

    genres = []  # List to store genre IDs
    languages = []  # List to store language IDs

    # Loop through each booking to extract genre and language info
    for booking in bookings:
        genres.extend([g.id for g in booking.movie.genre.all()])  # Add genre IDs
        languages.append(booking.movie.language.id)  # Add language ID

    # Get top 5 most common genre IDs
    top_genres = [g for g, _ in Counter(genres).most_common(5)]

    # Get top 5 most common language IDs
    top_languages = [l for l, _ in Counter(languages).most_common(5)]

    # Return dictionary containing top genres and languages
    return {
        'genre_ids': top_genres,
        'language_ids': top_languages
    }
