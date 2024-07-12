from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.utils.text import slugify

from config import settings

NULLABLE = {'blank': True, 'null': True}
User = get_user_model()


class Product(models.Model):
    """
    Модель, представляющая продукт в системе.

    Атрибуты:
        - name (CharField): Наименование продукта. Длина не должна превышать 100 символов.
        - description (TextField): Описание продукта. Может быть пустым или null.
        - preview (ImageField): Изображение продукта. Загружается в директорию 'products/'. Может быть пустым или null.
        - category (ForeignKey): Категория, к которой принадлежит продукт. Связь "многие ко одному" с моделью
                                 `Category`.
        - price (DecimalField): Цена продукта. Максимум 10 цифр с 2 десятичными знаками.
        - created_at (DateTimeField): Дата и время создания продукта. Устанавливается автоматически при создании.
        - updated_at (DateTimeField): Дата и время последнего обновления продукта. Устанавливается автоматически
                                      при каждом обновлении.
        - owner (ForeignKey): Владелец продукта, пользователь системы. Связь "многие к одному" с моделью `User`.

    Методы:
        - __str__(): Возвращает строковое представление продукта, которое является его наименованием.

    Класс Meta:
        - verbose_name: Человекочитаемое имя модели в единственном числе ('Продукт').
        - verbose_name_plural: Человекочитаемое имя модели во множественном числе ('Продукты').
    """

    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование продукта')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание продукта', **NULLABLE)
    preview = models.ImageField(upload_to='products/', verbose_name='Изображение',
                                help_text='Загрузите изображение продукта', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку',
                                help_text='Введите цену продукта')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    """
    Класс, представляющий модель Категории.

    Атрибуты:
    name (CharField): Наименование категории (максимальная длина - 100 символов).
    description (TextField): Описание категории. Может быть пустым (NULL).

    Методы:
    __str__() -> str: Возвращает строковое представление объекта (наименование категории).

    Вложенные классы:
    Meta:
        Класс метаданных для модели.
        verbose_name (str): Человекочитаемое имя модели в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.
    """

    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование категории')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание категории', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Contact(models.Model):
    """
    Класс, представляющий модель Контакта.

    Атрибуты:
    name (CharField): Имя контакта (максимальная длина - 100 символов).
    email (EmailField): E-mail адрес контакта.
    phone (CharField): Номер телефона контакта (максимальная длина - 20 символов).
    address (TextField): Адрес контакта.

    Методы:
    __str__() (str): Возвращает строковое представление объекта (имя контакта).

    Вложенные классы:
    Meta:
        Класс метаданных для модели.
        verbose_name (str): Человекочитаемое имя модели в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.
    """

    name = models.CharField(max_length=100, verbose_name="Имя", help_text="Введите Ваше имя")
    email = models.EmailField(verbose_name="E-mail", help_text="Введите Ваш E-mail")
    phone = models.CharField(max_length=20, verbose_name="Телефон", help_text="Введите Ваш номер телефона")
    address = models.TextField(verbose_name="Адрес", help_text="Введите Ваш адрес")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Blog(models.Model):
    """
    Класс, представляющий модель Статьи в блоге.

    Атрибуты:
    title (CharField): Заголовок статьи (максимальная длина - 200 символов).
    slug (SlugField): Слаг статьи (максимальная длина - 200 символов).
    content (TextField): Содержание статьи.
    preview (ImageField): Изображение для превью статьи (загружается в каталог 'blog/').
    created_at (DateTimeField): Дата и время создания статьи (автоматически заполняется при создании).
    is_published (BooleanField): Статус публикации статьи (по умолчанию - опубликована).
    views_count (PositiveIntegerField): Количество просмотров статьи (по умолчанию - 0).
    author_email (EmailField): E-mail автора статьи.

    Методы:
    __str__() (str): Возвращает строковое представление объекта (заголовок статьи).
    save(*args, **kwargs) (None): Сохраняет объект, при необходимости генерирует слаг и отправляет письмо при достижении
                                  100 просмотров.
    send_congratulation_email() (None): Отправляет поздравительное письмо автору статьи при достижении 100 просмотров.

    Вложенные классы:
    Meta:
        Класс метаданных для модели.
        verbose_name (str): Человекочитаемое имя модели в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок", help_text="Введите заголовок статьи")
    slug = models.SlugField(max_length=200)
    content = models.TextField(verbose_name="Содержание", help_text="Введите содержание статьи")
    preview = models.ImageField(upload_to='blog/', verbose_name="Изображение",
                                help_text="Загрузите изображение для превью статьи")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0)
    author_email = models.EmailField(verbose_name="E-mail автора", help_text="Введите E-mail автора статьи", **NULLABLE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.views_count == 100:
            self.send_congratulation_email()

    def send_congratulation_email(self):
        send_mail(
            'Поздравляем!',
            f'Ваша статья "{self.title}" набрала 100 просмотров!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.author_email],
            fail_silently=False,
        )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ProductVersion(models.Model):
    """
    Класс, представляющий модель Версии продукта.

    Атрибуты:
    product (ForeignKey): Ссылка на продукт, к которому относится версия (при удалении продукта, все связанные версии
                          также будут удалены).
    version_number (CharField): Номер версии продукта (максимальная длина - 10 символов).
    version_name (CharField): Название версии продукта (максимальная длина - 100 символов).
    is_current (BooleanField): Флаг, указывающий, является ли данная версия текущей (по умолчанию - False).

    Методы:
    __str__() (str): Возвращает строковое представление объекта (название версии).

    Вложенные классы:
    Meta:
        Класс метаданных для модели.
        verbose_name (str): Человекочитаемое имя модели в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions',
                                help_text='Введите версию продукта')
    version_number = models.CharField(max_length=10, verbose_name='Номер версии', help_text='Введите номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии', help_text='Введите название версии')
    is_current = models.BooleanField(default=False, verbose_name='Текущая версия')

    def __str__(self):
        return self.version_name

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продукта'
