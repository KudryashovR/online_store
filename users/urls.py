from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, VerifyEmailView, CustomLoginView, PasswordResetView, ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<int:user_id>/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
