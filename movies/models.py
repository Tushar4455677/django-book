from django.db import models
from django.contrib.auth.models import User

# Genre model to categorize movies (e.g., Action, Comedy)
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Language model to define the spoken language of a movie
class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Main Movie model containing all movie details
class Movie(models.Model):
    name = models.CharField(max_length=255)  # Movie name
    image = models.ImageField(upload_to="movies/")  # Poster image
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g., 8.5
    cast = models.TextField()  # Cast list as text
    description = models.TextField(blank=True, null=True)  # Optional movie description
    genre = models.ManyToManyField(Genre)  # Many genres per movie
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  # Language reference
    release_date = models.DateField()  # Release date

    def __str__(self):
        return self.name

# Theater model represents a specific show for a movie
class Theater(models.Model):
    name = models.CharField(max_length=255)  # Theater name
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')  # Linked movie
    time = models.DateTimeField()  # Show timing

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

# Seat model to define individual seats in a theater
class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')  # Belongs to a theater
    seat_number = models.CharField(max_length=10)  # e.g., A1, B2
    is_booked = models.BooleanField(default=False)  # Seat booking status

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

# Booking model stores information about user bookings
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who booked
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)  # One booking per seat
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Movie reference
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)  # Theater reference
    booked_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'
