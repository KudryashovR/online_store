from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView

from catalog.mixins import CustomLoginRequiredMixin
from config.settings import env, EMAIL_HOST_USER
from users.forms import CustomUserCreationForm, ProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_verification_email(user)
        return super(RegisterView, self).form_valid(form)

    @staticmethod
    def send_verification_email(user):
        send_mail("Verify your email", "Please verify your email by clicking the following link:\n" + env(
            'MY_IP_ADDRESS') + "/verify/{}/'".format(user.id), EMAIL_HOST_USER, [user.email],
                  fail_silently=False)


class VerifyEmailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        return HttpResponse("Email verified successfully")


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:home')


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            new_password = get_random_string(12)
            user.password = make_password(new_password)
            user.save()
            self.send_new_password_email(user, new_password)
        return HttpResponse("If the email exists in our system, a new password has been sent.")

    @staticmethod
    def send_new_password_email(user, new_password):
        send_mail("Your new password", f"Your new password is: {new_password}", EMAIL_HOST_USER, [user.email])


class ProfileUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self):
        return User.objects.get(email=self.request.user)
