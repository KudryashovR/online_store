# online_store

Проект интернет-магазина.

## Возможности

- Загрузка шаблонов домашней страницы и страницы контактной информации;
- Обработка POST запросов от пользователя на странице контактной информации и сохранение переданной информации в
  файл `messages.txt`;
- Вывод на главную страницу 5 последних добавленных товаров из базы данных;
- Вывод на страницу контактной информации данных из базы данных.

## Установка

1. Убедитесь, что у Вас установлены postgresql, [Poetry](https://python-poetry.org/docs/#installation) и Python 3.7 или
   выше.
2. Клонируйте репозиторий и перейдите в корневую директорию проекта:

```bash
git clone https://github.com/KudryashovR/online_store
cd online_store
```

3. Установите зависимости:

```bash
poetry install
```

## Настройка отправки почты

1. Создайте новый почтовый ящик на `mail.yandex.ru`
2. Настройте пароль для доступа через сторонние приложения
3. Создайте в корне проекта файл `.env` и запишите в нем:

```
EMAIL_HOST_USER='<your_mail>@yandex.ru'
EMAIL_HOST_PASSWORD='<your_mail_passvord>'
```

## Запуск

1. Создайте оболочку в виртуальной среде проекта:

```bash
poetry shell
```

2. Создайте базу данных `catalog` и, при необходимости, отредактируйте параметры подключения к БД в файле `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'catalog',
        'USER': 'postgres',
        'PASSWORD': '11235813',
    }
}
```

3. Проведите миграции:

```bash
python manage.py migrate
```

3. Запустите скрипт для первичного заполнения БД:

```bash
python manage.py initial_fill
```

4. Запустите сервер:

```bash
python manage.py runserver
```

## Лицензия

[MIT](LICENSE)
