from django.contrib import admin

# Из модуля models импортируем моделb Post, Group
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    """Модель админки."""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    # Перечисляем поля, которые должны отображаться в админке
    list_editable = ('group',)
    # Возможность изменять поле group в любом посте
    search_fields = ('text',)
    # Интерфейс для поиска по тексту постов
    list_filter = ('pub_date',)
    # Возможность фильтрации по дате
    empty_value_display = '-пусто-'
    # Свойство отображения пустых колонок


# При регистрации модели Post источником конфигурации для неё назначаем
# класс PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group)
