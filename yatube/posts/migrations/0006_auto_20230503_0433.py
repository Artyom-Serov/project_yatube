# Generated by Django 2.2.19 on 2023-05-03 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20230418_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(help_text='Описание особенности группы', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Выберите уникальный адрес для группы', null=True, unique=True, verbose_name='Адрес группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='Введите название группы', max_length=200, verbose_name='Название'),
        ),
    ]
