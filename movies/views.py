from django.shortcuts import render, redirect, get_object_or_404  # Functions to render templates and handle object lookups
from django.contrib.auth.decorators import login_required  # Decorator to restrict views to logged-in users
from django.db import IntegrityError  # To catch duplicate booking errors
from movies.models import Movie, Theater, Seat, Booking, Genre, Language  # Importing movie-related models
from movies.utils import get_user_preferences  # Utility to fetch user's movie preferences
from collections import Counter  # To count most frequent genres/languages
from django.db.models import Q  # To build complex query filters

#  Movie List View with Search Support
def movie_list(request):
    movies = Movie.objects.all()  # Fetch all movies
    genres = Genre.objects.all()  # Fetch all genres
    languages = Language.objects.all()  # Fetch all languages

    # Get genre and language filters from URL query parameters
    genre_filter = request.GET.get('genre')
    language_filter = request.GET.get('language')

    # Filter movies by selected genre
    if genre_filter:
        movies = movies.filter(genre__id=genre_filter)

    # Filter movies by selected language
    if language_filter:
        movies = movies.filter(language__id=language_filter)

    # Render the movie list page with filters
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'languages': languages,
    })

#  List of Theaters for Selected Movie
def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)  # Get the movie or return 404
    theaters = Theater.objects.filter(movie=movie)  # Get all theaters showing the movie
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

#  Seat Booking Page (View + Book Seats)
@login_required(login_url='/login/')  # Restrict access to logged-in users
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)  # Get the theater or return 404
    seats = Seat.objects.filter(theater=theater)  # Get all seats for the theater

    # Handle POST request for booking seats
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')  # Get selected seat IDs
        error_seats = []  # List to store already booked seat numbers

        # If no seat selected, show error
        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                'theater': theater,
                "seats": seats,
                'error': " No seat selected!"
            })

        # Loop through selected seats and attempt booking
        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)  # Get seat object
            if seat.is_booked:
                error_seats.append(seat.seat_number)  # Skip already booked seats
                continue
            try:
                # Create booking and mark seat as booked
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)  # Handle race condition booking

        # If any seats failed to book, show error message
        if error_seats:
            error_message = f" Already booked: {', '.join(error_seats)}"
            return render(request, "movies/seat_selection.html", {
                'theater': theater,
                "seats": seats,
                'error': error_message
            })

        #  Booking successful, redirect to profile page
        return redirect('profile')

    # GET Request: Show seat selection page
    return render(request, "movies/seat_selection.html", {
        'theater': theater,
        "seats": seats
    })

#  Recommended Movies Based on User Preferences
def recommended_movies(request):
    user = request.user  # Get the logged-in user
    preferences = get_user_preferences(user)  # Get user's genre and language preferences
    booked_movie_ids = Booking.objects.filter(user=user).values_list('movie_id', flat=True)  # Get already booked movies

    # Fetch movies matching preferred genres or languages, excluding already booked ones
    recommended = Movie.objects.filter(
        Q(genre__id__in=preferences['genre_ids']) |
        Q(language__id__in=preferences['language_ids'])
    ).exclude(
        id__in=booked_movie_ids
    ).distinct()  # Avoid duplicates due to multiple genres/languages

    # Render the recommended movies page
    return render(request, 'recommended.html', {
        'movies': recommended,
        'booked_movies': list(booked_movie_ids)
    })
