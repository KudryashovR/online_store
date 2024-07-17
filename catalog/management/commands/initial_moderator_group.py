from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """
    Команда Django для создания или обновления группы 'Модератор' с заданными правами доступа.

    Методы:
        - handle(*args, **kwargs): Основной метод, который выполняет логику создания или обновления группы и добавления
                                   прав доступа.
    """

    def handle(self, *args, **kwargs):
        """
        Создает или обновляет группу 'Модератор' с необходимыми правами доступа.

        При выполнении команды, если группа 'Модератор' не существует, она будет создана. Затем к группе будут добавлены
        следующие права доступа:
        - can_cancel_publication (может отменять публикацию)
        - can_change_description (может изменять описание)
        - can_change_category (может изменять категорию)

        После успешного выполнения команда выводит сообщение об успешном создании или обновлении группы.

        Параметры:
            - *args: Дополнительные позиционные аргументы.
            - **kwargs: Дополнительные именованные аргументы.
        """

        group, created = Group.objects.get_or_create(name='Модератор')

        permissions = [
            Permission.objects.get(codename='can_cancel_publication'),
            Permission.objects.get(codename='can_change_description'),
            Permission.objects.get(codename='can_change_category'),
        ]

        for perm in permissions:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Successfully created/updated Модератор group'))
