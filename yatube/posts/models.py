from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel

User = get_user_model()
"""Обращаемся к модели User через функцию get_user_model."""


class Post(CreatedModel):
    """Модель постов."""
    text = models.TextField(verbose_name='Запись',
                            help_text='Место для вашей записи')
    # Поле для хранения произвольного текста
    created = models.DateTimeField(auto_now_add=True,
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
    # Поле для картинки (необязательное)
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        help_text='Выберите изображение для поста'
    )

    class Meta:
        ordering = ['-created', ]
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


class Comment(CreatedModel):
    """Модель комментариев."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
        help_text='Пост, к которому написан комментарий'
    )
    # Поле для связи комментариев с постом, со ссылкой на модель Post.
    # параметр *on_delete=models.CASCADE* обеспечивает связность данных:
    # если из таблицы Post будет удалён пост, то будут удалены все
    # связанные с ним комментарии.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    # Поле для связи комментариев с пользователем, со ссылкой на модель User.
    # параметр *on_delete=models.CASCADE* обеспечивает связность данных:
    # если из таблицы User будет удалён пользователь,
    # то будут удалены все связанные с ним комментарии.
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите текст вашего комментария')
    # Поле для хранения текста комментария.
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    # Поле для хранения даты и времени создания комментария.

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
