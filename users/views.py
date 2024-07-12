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
    """
    Представление для регистрации новых пользователей.

    Это представление использует форму CustomUserCreationForm для создания новой учетной записи пользователя.
    После успешной регистрации пользователю отправляется письмо с просьбой подтвердить свой email.

    Атрибуты:
    ----------
    model : Model
        Модель, с которой связано это представление (User).
    form_class : Form
        Класс формы, используемый для создания нового пользователя (CustomUserCreationForm).
    template_name : str
        Имя шаблона, используемого для отображения формы регистрации ('users/register.html').
    success_url : URL
        URL для перенаправления после успешной регистрации (reverse_lazy('users:login')).

    Методы:
    -------
    form_valid(form):
        Метод, который вызывается при отправке и валидации формы.
        Сохраняет пользователя с установленным is_active=False и отправляет письмо с верификацией.
    send_verification_email(user):
        Статический метод для отправки письма с верификацией на email пользователя.
    """

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
    """
    Представление для верификации email пользователя.

    Это представление обрабатывает GET-запросы для завершения процесса верификации email.
    При успешной верификации активируется учетная запись пользователя.

    Методы:
    -------
    get(request, user_id):
        Обрабатывает GET-запрос. Активирует учетную запись пользователя и возвращает сообщение
        о успешной верификации email.
    """

    def get(self, request, user_id):
        """
        Обрабатывает GET-запрос для верификации email.

        Параметры:
        ----------
        request : HttpRequest
            Объект запроса.
        user_id : int
            Идентификатор пользователя, который должен быть верифицирован.

        Возвращает:
        -----------
        HttpResponse
            Возвращает сообщение о успешной верификации email.
        """

        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()

        return HttpResponse("Email verified successfully")


class CustomLoginView(LoginView):
    """
    Пользовательское представление для входа в систему.

    Это представление расширяет стандартное представление Django для входа в систему, предоставляя
    дополнительные возможности, такие как перенаправление аутентифицированных пользователей и указание
    пользовательского шаблона для страницы входа.

    Атрибуты класса:
    -----------------
    template_name : str
        Имя шаблона, который будет использоваться для отображения страницы входа. По умолчанию 'users/login.html'.
    redirect_authenticated_user : bool
        Флаг, указывающий, следует ли перенаправлять аутентифицированных пользователей. По умолчанию True.

    Методы:
    -------
    get_success_url():
        Возвращает URL, на который будет перенаправлен пользователь после успешного входа. В данном
        случае переадресация идет на главную страницу каталога.
    """

    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного входа.

        Возвращает:
        -----------
        str
            URL на главную страницу каталога ('catalog:home').
        """

        return reverse_lazy('catalog:home')


class PasswordResetView(View):
    """
    Представление для сброса пароля пользователя.

    Это представление обрабатывает как GET, так и POST запросы для сброса пароля. При получении
    POST-запроса с адресом электронной почты пользователя, система генерирует новый пароль и отправляет
    его на указанный адрес электронной почты, если такой пользователь существует.

    Методы:
    -------
    get(request):
        Отображает страницу сброса пароля.

    post(request):
        Обрабатывает запрос на сброс пароля. Генерирует новый пароль и отправляет его пользователю, если
        указанный адрес электронной почты найден в системе.

    send_new_password_email(user, new_password):
        Статический метод для отправки нового пароля пользователю на электронную почту.
    """

    def get(self, request):
        """
        Отображает страницу сброса пароля.

        Параметры:
        ----------
        request : HttpRequest
            Объект запроса.

        Возвращает:
        -----------
        HttpResponse
            Ответ с отрендеренной страницей сброса пароля.
        """

        return render(request, 'users/password_reset.html')

    def post(self, request):
        """
        Обрабатывает запрос на сброс пароля.

        Если пользователь с указанным адресом электронной почты существует, генерируется
        новый пароль, сохраняется и отправляется на электронную почту пользователя.

        Параметры:
        ----------
        request : HttpRequest
            Объект запроса, содержащий данные формы.

        Возвращает:
        -----------
        HttpResponse
            Ответ с подтверждением отправки нового пароля.
        """

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
        """
        Отправляет новый пароль на электронную почту пользователя.

        Параметры:
        ----------
        user : User
            Экземпляр пользователя, чей пароль был сброшен.
        new_password : str
            Новый сгенерированный пароль.
        """

        send_mail("Your new password", f"Your new password is: {new_password}", EMAIL_HOST_USER, [user.email])


class ProfileUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    Представление для обновления профиля пользователя.

    Это представление позволяет авторизованным пользователям обновлять свои данные профиля.
    Представление наследуется от `CustomLoginRequiredMixin` для проверки аутентификации
    пользователя и от `UpdateView` для использования встроенных функций обновления записи.

    Атрибуты класса:
    ----------------
    model : Model
        Модель, которую необходимо обновить (в данном случае, модель User).
    form_class : ModelForm
        Форма, используемая для обновления профиля пользователя.
    template_name : str
        Имя шаблона, используемого для отображения формы.
    success_url : str
        URL-адрес, на который будет перенаправлен пользователь после успешного обновления профиля.

    Методы:
    -------
    get_object(self):
        Возвращает текущий объект пользователя, который будет обновляться.
    """

    model = User
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self):
        """
        Возвращает текущий объект пользователя.

        Этот метод используется для получения объекта пользователя, который
        будет редактироваться, на основе текущего аутентифицированного пользователя.

        Возвращает:
        -----------
        User
            Экземпляр текущего аутентифицированного пользователя.
        """

        return User.objects.get(email=self.request.user)
