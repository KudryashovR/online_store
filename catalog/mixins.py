from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin класс, обеспечивающий требование авторизации для доступа к представлениям.

    Этот класс расширяет функционал `LoginRequiredMixin` из Django, добавляя кастомный URL для редиректа на страницу
    входа.

    Атрибуты класса:
        - login_url (str): URL-адрес, на который будет произведен редирект, если пользователь не аутентифицирован.
                           Здесь он указывает на именованный URL 'users:login'.
    """

    login_url = reverse_lazy('users:login')
