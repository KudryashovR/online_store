# online_store

Проект интернет-магазина.

## Возможности

- Загрузка шаблонов домашней страницы и страницы контактной информации;
- Обработка POST запросов от пользователя на странице контактной информации и сохранение переданной информации в
  файл `messages.txt`

## Установка

1. Убедитесь, что у Вас установлены [Poetry](https://python-poetry.org/docs/#installation) и Python 3.7 или выше.
2. Клонируйте репозиторий и перейдите в корневую директорию проекта:

```bash
git clone https://github.com/KudryashovR/online_store
cd online_store
```

3. Установите зависимости:

```bash
poetry install
```

## Запуск

1. Создайте оболочку в виртуальной среде проекта:

```bash
poetry shell
```

2. Запустите сервер:

```bash
python manage.py runserver
```

## Лицензия

[MIT](LICENSE)