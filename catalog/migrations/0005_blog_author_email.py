# Generated by Django 5.0.6 on 2024-06-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_blog_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author_email',
            field=models.EmailField(blank=True, help_text='Введите E-mail автора статьи', max_length=254, null=True, verbose_name='E-mail автора'),
        ),
    ]