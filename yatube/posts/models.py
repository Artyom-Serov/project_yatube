from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
"""Обращаемся к модели User через функцию get_user_model."""


class Group(models.Model):
    """Модель групп."""
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    # Название группы
    slug = models.SlugField(
        null=True,
        unique=True,
        verbose_name='Адрес группы'
    )
    # Уникальный адрес группы
    description = models.TextField(
        verbose_name='Описание'
    )
    # Tекст, описывающий сообщество

    class Meta:
        ordering = ('title',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель постов."""
    text = models.TextField()
    # Поле для хранения произвольного текста
    pub_date = models.DateTimeField(auto_now_add=True)
    # Поле для хранения даты и времени
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    # Поле для хранения автора, со ссылкой на модель User.
    # араметр *on_delete=models.CASCADE* обеспечивает
    # связность данных: если из таблицы User будет удалён пользователь,
    # то будут удалены все связанные с ним посты.
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('text',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
