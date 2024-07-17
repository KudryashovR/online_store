from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Контент-менеджер')

        permissions = [
            Permission.objects.get(codename='add_blog'),
            Permission.objects.get(codename='change_blog'),
            Permission.objects.get(codename='delete_blog'),
            Permission.objects.get(codename='view_blog'),
        ]

        for perm in permissions:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Successfully created/updated Контент-менеджер group'))
