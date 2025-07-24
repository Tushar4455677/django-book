from django.urls import path  # Importing path to define URL patterns
from .views import register, login_view, profile, reset_password, home  # Importing custom user views

from django.contrib.auth import views as auth_views  # Importing Django's built-in auth views with alias

urlpatterns = [
    path('', home, name='home'),  # Home page route (Note: this may be better handled as path('', ...) in practice)
    path('register/', register, name='register'),  # User registration page
    path('profile/', profile, name='profile'),  # User profile page
    path('change_password/', reset_password, name='change_password'),  # Custom password change view

    # Logout view using Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Password reset request form
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'),
         name='password_reset'),

    # Confirmation page after submitting email for password reset
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    # Password reset form with UID and token from email link
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # Final confirmation page after password has been reset
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    # Login view using Django's built-in LoginView
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]
