from django import forms

from .models import Product, ProductVersion

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    """
    Класс ProductForm представляет собой форму для модели Product.

    Вложенный класс Meta:
        - model: Указывает модель, для которой создается форма (в данном случае, модель Product).
        - fields (list): Определяет список полей модели, которые будут включены в форму. Здесь это поля 'name',
                         'description', 'preview', 'category' и 'price'.

    Методы:
        - clean_name: Метод валидации для поля 'name'. Проверяет, что в названии продукта не содержатся запрещенные
                      слова. Если запрещенное слово найдено, вызывается исключение ValidationError.
        - clean_description: Метод валидации для поля 'description'. Проверяет, что в описании продукта не содержатся
                             запрещенные слова. Если запрещенное слово найдено, вызывается исключение ValidationError.

    Переменные:
        - FORBIDDEN_WORDS (list): Список слов, которые запрещены для использования в названии и описании продукта.
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'preview', 'category', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f"Запрещенное слово в названии: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f"Запрещенное слово в описании: {word}")
        return description


class VersionForm(forms.ModelForm):
    """
    Класс VersionForm представляет собой форму для модели ProductVersion.

    Вложенный класс Meta:
        - model: Указывает модель, для которой создается форма (в данном случае, модель ProductVersion).
        - fields (list): Определяет список полей модели, которые будут включены в форму. Здесь это поля 'product',
                         'version_number', 'version_name' и 'is_current'.

    Переменные:
        - product (ForeignKey): Ссылка на продукт, к которому относится данная версия.
        - version_number (CharField): Номер версии продукта.
        - version_name (CharField): Имя версии продукта.
        - is_current (BooleanField): Флаг, указывающий, является ли данная версия текущей.
    """

    class Meta:
        model = ProductVersion
        fields = ['product', 'version_number', 'version_name', 'is_current']
