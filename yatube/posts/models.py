from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
"""Обращаемся к модели User через функцию get_user_model."""


class Post(models.Model):
    """Модель постов."""
    text = models.TextField(verbose_name='Запись',
                            help_text='Место для вашей записи')
    # Поле для хранения произвольного текста
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата создания'
                                    )
    # Поле для хранения даты и времени
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    # Поле для хранения автора, со ссылкой на модель User.
    # параметр *on_delete=models.CASCADE* обеспечивает
    # связность данных: если из таблицы User будет удалён пользователь,
    # то будут удалены все связанные с ним посты.
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу для публикации'
    )
    # Поле для хранения группы, со ссылкой на модель Group.
    # параметр *on_delete=models.SET_NULL* обеспечивает
    # связность данных: если из таблицы Group будет удалена группа,
    # то в поле ссылки на группу будет значение NULL.

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    """Модель групп."""
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название группы'
    )
    # Название группы
    slug = models.SlugField(
        null=True,
        unique=True,
        verbose_name='Адрес группы',
        help_text='Выберите уникальный адрес для группы'
    )
    # Уникальный адрес группы
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание особенности группы'
    )
    # Tекст, описывающий сообщество

    class Meta:
        ordering = ['title', ]
        # Параметр сортировки отображения по умолчанию
        # по полю *title*
        verbose_name = 'Группа'
        # Параметр для отображения поля на русском языке
        verbose_name_plural = 'Группы'
        # Параметр для отображения поля на русском языке,
        # если поле во множественном числе

    def __str__(self):
        return self.title
