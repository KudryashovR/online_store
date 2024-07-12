from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя с кастомными полями.

    Наследует:
    ----------
    UserCreationForm : форма
        Базовая форма для создания новых пользователей, предоставляемая Django.

    Атрибуты класса Meta:
    ---------------------
    model : Model
        Модель, с которой работает данная форма (User).
    fields : tuple
        Поля модели, которые будут использоваться в форме ('email', 'password1', 'password2').

    Описание:
    ---------
    Эта форма используется для регистрации новых пользователей, требуя от них
    указания адреса электронной почты и дважды ввода пароля для его подтверждения.
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    """
    Форма для обновления профиля пользователя и изменения пароля.

    Поля формы:
    -----------
    old_password : CharField
        Поле для ввода старого пароля пользователя.
    new_password1 : CharField
        Поле для ввода нового пароля.
    new_password2 : CharField
        Поле для подтверждения нового пароля.

    Методы:
    -------
    clean():
        Проверяет совпадение новых паролей. Если пароли не совпадают, добавляет ошибку в поле 'new_password2'.

    Атрибуты класса Meta:
    ---------------------
    model : Model
        Модель, с которой работает данная форма (User).
    fields : tuple
        Поля модели, которые будут использоваться в форме ('email', 'avatar', 'phone', 'country').

    Описание:
    ---------
    Эта форма используется для обновления информации профиля пользователя, включая
    адрес электронной почты, аватар, номер телефона и страну, а также для изменения пароля.
    """

    old_password = forms.CharField(widget=forms.PasswordInput, label='Старый пароль')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите новый пароль')

    def clean(self):
        cleaned_data = super().clean()

        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "Пароли не совпадают")

        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country')
