# online_store

Проект интернет-магазина.

## Возможности

- Загрузка шаблонов домашней страницы, страницы контактной информации, страницы блога и страницы редактирования профиля пользователя;
- Обработка POST запросов от пользователя на странице контактной информации и сохранение переданной информации в
  файл `messages.txt`;
- Вывод на главную страницу товаров из базы данных;
- Вывод на страницу контактной информации данных из базы данных;
- Вывод страницы блога;
- Добавление новых товаров;
- Добавление, изменение и удаление статей блога;
- Отправка уведомления на адрес электронной почты при достижении статьей 100 просмотров.
- Вывод на страницу товара версии.
- Регистрация и аутентификация пользователей, сброс пароля.

## Установка

1. Убедитесь, что у Вас установлены postgresql, [Poetry](https://python-poetry.org/docs/#installation), Redis и Python 3.7 или
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
DATABASES_NAME='<your_db_name>'
DATABASES_USER='<your_db_user>'
DATABASES_PASSWORD='<your_db_user_password>'
EMAIL_HOST_USER='<your_mail>@yandex.ru'
EMAIL_HOST_PASSWORD='<your_mail_passvord>'
MY_IP_ADDRESS='<IP-address>'
```

## Запуск

1. Создайте оболочку в виртуальной среде проекта:

```bash
poetry shell
```

2. Создайте базу данных `catalog` и отредактируйте параметры подключения к БД в файле `.env`:

```
DATABASES_NAME='catalog'
DATABASES_USER='<your_DB_user>'
DATABASES_PASSWORD='<you_password_for_DB_user>'
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
