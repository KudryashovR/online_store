from django.contrib import admin

from catalog.models import Category, Product, Contact, Blog, ProductVersion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Класс CategoryAdmin представляет собой административную конфигурацию для модели Category в Django Admin.
    Он определяет, какие поля модели должны быть отображены в списке объектов в административной панели.

    Атрибуты:
        - list_display: Кортеж, определяющий, какие поля модели будут отображены в списке объектов в административной
                        панели. В данном случае, это поля id и name.
    """

    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс ProductAdmin представляет собой конфигурацию административного интерфейса для модели Product.

    Атрибуты:
        - list_display (tuple): Определяет поля модели, которые будут отображены в списке объектов в административной
                                панели. В данном случае отображаются поля 'id', 'name', 'price', 'category'.
        - list_filter (tuple): Определяет поля модели, по которым можно фильтровать объекты в административной панели.
                               В данном случае фильтрация доступна по полю 'category'.
        - search_fields (tuple): Определяет поля модели, по которым можно осуществлять поиск объектов в административной
                                 панели. В данном случае поиск доступен по полям 'name' и 'description'.
    """

    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Класс ContactAdmin представляет собой конфигурацию административного интерфейса для модели Contact.

    Атрибуты:
        - list_display (tuple): Определяет поля модели, которые будут отображены в списке объектов в административной
                                панели. В данном случае отображаются поля 'id' и 'name'.
        - search_fields (tuple): Определяет поля модели, по которым можно осуществлять поиск объектов в административной
                                 панели. В данном случае поиск доступен по полю 'name'.
    """

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Класс BlogAdmin представляет собой конфигурацию административного интерфейса для модели Blog.

    Атрибуты:
        - list_display (tuple): Определяет поля модели, которые будут отображены в списке объектов в административной
        панели. В данном случае отображаются поля 'id', 'title' и 'is_published'.
        - list_filter (tuple): Определяет поля модели, по которым можно фильтровать объекты в административной панели.
                               В данном случае можно фильтровать по полю 'is_published'.
        - search_fields (tuple): Определяет поля модели, по которым можно осуществлять поиск объектов в административной
                                 панели. В данном случае поиск доступен по полям 'title' и 'content'.
    """

    list_display = ('id', 'title', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    """
    Класс ProductVersionAdmin представляет собой конфигурацию административного интерфейса для модели ProductVersion.

    Атрибуты:
        - list_display (tuple): Определяет поля модели, которые будут отображены в списке объектов в административной
        панели. В данном случае отображаются поля 'id', 'version_number', 'product' и 'is_current'.
        - list_filter (tuple): Определяет поля модели, по которым можно фильтровать объекты в административной панели.
                               В данном случае можно фильтровать по полю 'is_current'.
        - search_fields (tuple): Определяет поля модели, по которым можно осуществлять поиск объектов в административной
                                 панели. В данном случае поиск доступен по полю 'product__name', что позволяет искать
                                 по имени связанного продукта.
    """

    list_display = ('id', 'version_number', 'product', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('product__name',)
