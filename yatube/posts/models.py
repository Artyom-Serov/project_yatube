from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
"""Обращаемся к модели User через функцию get_user_model."""


class Post(models.Model):
    text = models.TextField()
    """Поле для хранения произвольного текста."""
    pub_date = models.DateTimeField(auto_now_add=True)
    """Поле для хранения даты и времени."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    """Поле для хранения автора, со ссылкой на модель User.
    Параметр *on_delete=models.CASCADE* обеспечивает
    связность данных: если из таблицы User будет удалён пользователь,
    то будут удалены все связанные с ним посты.
    """


class Group(models.Model):
    pass
