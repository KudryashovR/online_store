from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """
    Класс Command предназначен для удаления всех существующих категорий и товаров из базы данных, а затем для создания
    новых категорий и соответствующих товаров.

    Атрибуты:
        - stdout - Стандартный вывод для команды, используется для отображения сообщений пользователю во время
                   выполнения команды.

    Методы:
        - handle(self, *args, **options): Основной метод, который выполняет следующие шаги:
            - Печатает сообщение о начале удаления категорий и товаров.
            - Удаляет все записи из моделей Category и Product.
            - Печатает сообщение о начале создания новых данных.
            - Создает новые категории и сохраняет их в базу данных.
            - Печатает сообщение о успешном создании категорий.
            - Создает новые товары, связывая их с созданными категориями, и сохраняет их в базу данных.
            - Печатает сообщение о успешном создании товаров.
            - Печатает сообщение о завершении и успешном заполнении базы данных новыми данными.
    """

    def handle(self, *args, **options):
        self.stdout.write('Удаление всех категорий и товаров...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Создание новых данных...')

        categories_data = [
            {"name": "Электроника", "description": "Товары, относящиеся к категории электроники"},
            {"name": "Одежда", "description": "Различная одежда для всех возрастов"},
            {"name": "Продукты питания", "description": "Еда и напитки"},
            {"name": "Книги", "description": "Художественная и научная литература"},
            {"name": "Игрушки", "description": "Детские игрушки для разных возрастов"},
        ]

        categories = [
            Category(name=data["name"], description=data["description"])
            for data in categories_data
        ]

        Category.objects.bulk_create(categories)

        self.stdout.write('Категории успешно созданы!')

        products_data = [
            {"name": "Смартфон", "description": "Мобильный телефон с сенсорным экраном", "category": "Электроника",
             "price": 50000.00},
            {"name": "Джинсы", "description": "Синие джинсы из денима", "category": "Одежда", "price": 1500.00},
            {"name": "Хлеб", "description": "Свежий хлеб из пекарни", "category": "Продукты питания", "price": 50.00},
            {"name": "Роман", "description": "Книга в жанре роман", "category": "Книги", "price": 300.00},
            {"name": "Лего", "description": "Конструктор Лего", "category": "Игрушки", "price": 1000.00},
        ]

        for data in products_data:
            category = Category.objects.get(name=data["category"])
            Product.objects.create(name=data["name"], description=data["description"], category=category,
                                   price=data["price"])

        self.stdout.write('Товары успешно созданы!')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена новыми данными!'))
