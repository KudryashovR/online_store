from django import forms
from django.db import models

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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'preview', 'category', 'price'
        ]
