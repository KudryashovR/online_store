from django.core.cache import cache

from catalog.models import Product


def get_cached_products():
    """
    Получает список продуктов из кэша или базы данных.

    Проверяет наличие списка продуктов в кэше под ключом 'products_list'. Если список продуктов отсутствует в кэше,
    загружает его из базы данных, сохраняет в кэш и возвращает.

    Возвращает:
        list: Список объектов Product.
    """

    products = cache.get('products_list')

    if not products:
        products = list(Product.objects.all())
        cache.set('products_list', products)

    return products
