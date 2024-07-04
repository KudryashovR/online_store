from django.core.mail import send_mail
from django.db import models
from django.utils.text import slugify

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование продукта')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание продукта', **NULLABLE)
    preview = models.ImageField(upload_to='products/', verbose_name='Изображение',
                                help_text='Загрузите изображение продукта', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку',
                                help_text='Введите цену продукта')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование категории')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание категории', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Contact(models.Model):
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
