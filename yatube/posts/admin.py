from django.contrib import admin

# Из модуля models импортируем моделb Post, Group
from .models import Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Модель администрирования постов."""
    list_display = (
        'pk',
        'text',
        'created',
        'author',
        'group',
    )
    # Перечисляем поля, которые должны отображаться в админке
    list_editable = ('group',)
    # Возможность изменять поле group в любом посте
    search_fields = ('text',)
    # Интерфейс для поиска по тексту постов
    list_filter = ('created',)
    # Возможность фильтрации по дате
    empty_value_display = '-пусто-'
    # Свойство отображения пустых колонок


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Модель администрирования групп."""
    list_display = (
        'title',
        'slug',
        'description',
    )
    # отображаемые поля в админке
    search_fields = ('slug',)
    # Интерфейс для поиска по слагу
    list_filter = ('title',)
    # Возможность фильтрации по названию группы
    empty_value_display = '-пусто-'
    # Свойство отображения пустых колонок


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель администрирования комментариев."""
    list_display = (
        'post',
        'author',
        'text',
        'created',
    )
    # отображаемые поля в админке
    list_filter = ('author', 'text', 'created')
    # Возможность фильтрации по названию автору,
    # полю коментариев и дате создания
    search_fields = ('post', 'author', 'text')
    # Интерфейс для поиска по заданым полям


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Модель администрирования подписок."""
    list_display = ('user', 'author')
    # отображаемые поля в админке
    list_filter = ('user', 'author')
    # Возможность фильтрации по названию автору и подписчику
    search_fields = ('user', 'author')
    # Интерфейс для поиска по заданым полям
