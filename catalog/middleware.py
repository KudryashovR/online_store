from django.utils.cache import add_never_cache_headers


class ExcludeCacheMiddleware:
    """
    Middleware для исключения кеширования определенных URL.

    Этот middleware проверяет запросы поступающие на сервер, и если  путь запроса соответствует одному из заданных URL,
    добавляет к ответу заголовки, предотвращающие кеширование. Это позволяет обеспечить актуальность данных
    для ресурсов, которые часто меняются, таких как страницы продуктов и новых блогов.

    Атрибуты:
        get_response (function): Функция, которая обрабатывает запрос и возвращает ответ.
    """

    def __init__(self, get_response):
        """
        Инициализатор класса.

        Параметры:
            get_response (function): Функция, которая обрабатывает запрос и возвращает ответ.
        """

        self.get_response = get_response

    def __call__(self, request):
        """
        Обработка входящего запроса.

        Параметры:
            request (HttpRequest): Входящий HTTP запрос.

        Возвращает:
            HttpResponse: HTTP ответ с или без заголовков, предотврающих кеширование.
        """

        response = self.get_response(request)

        if any(url in request.path for url in ['', 'product/', 'new_product', 'blog/new/']):
            add_never_cache_headers(response)

        return response
