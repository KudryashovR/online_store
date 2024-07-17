from django import forms

from .models import Product, ProductVersion

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    """
    Форма для модели Product, адаптированная для фильтрации полей на основе прав пользователя.

    Параметры:
        - user_id (User, optional): Объект пользователя для проверки прав на доступ к определенным полям.

    Атрибуты:
        - available_fields (list): Список полей, доступных для пользователя в зависимости от его прав доступа.

    Методы:
        - __init__(user_id=None, *args, **kwargs): Инициализирует форму и фильтрует доступные поля на основе прав
                                                   пользователя.
        - clean_name(): Проверяет поле 'name' на наличие запрещенных слов и выбрасывает ValidationError, если запретные
                        слова найдены.
        - clean_description(): Проверяет поле 'description' на наличие запрещенных слов и выбрасывает ValidationError,
                               если запретные слова найдены.

    Класс Meta:
        - model (Product): Связанная модель Django.
        - fields (list): Полный список полей формы, который позднее может фильтроваться на основе прав пользователя.
    """

    def __init__(self, user_id=None, *args, **kwargs):
        """
        Инициализация формы с возможностью фильтрации полей на основе прав пользователя.

        Параметры:
            - user_id (User, optional): Объект пользователя для проверки прав на доступ к определенным полям.
            - *args: Аргументы для функции-родителя.
            - **kwargs: Именованные аргументы для функции-родителя.
        """

        super(ProductForm, self).__init__(*args, **kwargs)

        available_fields = ['name', 'preview', 'price']

        if user_id:
            if user_id.has_perm('catalog.can_cancel_publication'):
                available_fields.append('is_published')
            if user_id.has_perm('catalog.can_change_description'):
                available_fields.append('description')
            if user_id.has_perm('catalog.can_change_category'):
                available_fields.append('category')

        self.fields = {
            key: self.fields[key] for key in available_fields
        }

    class Meta:
        model = Product
        fields = ['name', 'description', 'preview', 'category', 'price', 'is_published']

    def clean_name(self):
        """
        Проверяет поле 'name' на наличие запрещенных слов.

        Возвращает:
            - str: Возвращает очищенное значение поля 'name'.

        Исключения:
            - ValidationError: Если найдено запрещенное слово в названии.
        """

        name = self.cleaned_data.get('name')
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f"Запрещенное слово в названии: {word}")
        return name

    def clean_description(self):
        """
        Проверяет поле 'description' на наличие запрещенных слов.

        Возвращает:
            - str: Возвращает очищенное значение поля 'description'.

        Исключения:
            - ValidationError: Если найдено запрещенное слово в описании.
        """

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
