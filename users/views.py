from django.conf import settings  # To access project-level settings like email config

from django.shortcuts import render, redirect  # For rendering templates and redirecting
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm  # Built-in forms for login and password change
from .forms import UserRegisterForm, UserUpdateForm  # Custom user registration and update forms
from django.contrib.auth import login, authenticate, update_session_auth_hash  # Authentication and session functions
from django.contrib.auth.decorators import login_required  # To protect views with login requirement
from movies.models import Movie, Booking, Genre, Language  # Import models for use in views
from django.core.mail import send_mail  # For sending email via contact form
from django.contrib import messages  # To show success messages in templates

# Static About Page View
def about_view(request):
    return render(request, 'about.html')  # Render the about page

# Contact Page View with Email Sending Logic
def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']  # Get name from form
        email = request.POST['email']  # Get email from form
        message = request.POST['message']  # Get message from form

        # Send email to configured host user
        send_mail(
            subject=f" Contact Message from {name}",
            message=message,
            from_email=email,
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        # Show success message and redirect to contact page
        messages.success(request, " Message sent successfully! Thank you for your contacts and ratings.")
        return redirect('contact')

    return render(request, 'contact.html')  # Render the contact page for GET request

# Homepage View - Display All Movies
def home(request):
    movies = Movie.objects.all()  # Fetch all movies from DB
    return render(request, 'home.html', {'movies': movies})  # Render homepage with movies

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Bind form with POST data
        if form.is_valid():
            form.save()  # Save new user
            username = form.cleaned_data.get('username')  # Get username
            password = form.cleaned_data.get('password1')  # Get password
            user = authenticate(username=username, password=password)  # Authenticate user
            login(request, user)  # Log in user
            return redirect('profile')  # Redirect to profile page
    else:
        form = UserRegisterForm()  # Unbound form for GET request
    return render(request, 'users/register.html', {'form': form})  # Render registration form

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Bind form with login data
        if form.is_valid():
            user = form.get_user()  # Get authenticated user
            login(request, user)  # Log in user
            return redirect('profile')  # Redirect to profile
    else:
        form = AuthenticationForm()  # Unbound form for GET request
    return render(request, 'users/login.html', {'form': form})  # Render login form

# Profile View with User Info and Booking History
@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'theater', 'seat')  # Fetch user's bookings
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)  # Form bound to current user
        if u_form.is_valid():
            u_form.save()  # Save updated user info
            return redirect('profile')  # Redirect to profile
    else:
        u_form = UserUpdateForm(instance=request.user)  # Unbound form for GET request
        
    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'bookings': bookings  # Pass bookings to template
    })

# Password Change View
@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)  # Bind form with POST data
        if form.is_valid():
            user = form.save()  # Save new password
            update_session_auth_hash(request, user)  # Prevent user logout after password change
            return redirect('login')  # Redirect to login
    else:
        form = PasswordChangeForm(user=request.user)  # Unbound form for GET request
    return render(request, 'users/reset_password.html', {'form': form})  # Render password change form
