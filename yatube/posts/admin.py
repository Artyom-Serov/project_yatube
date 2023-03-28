from django.contrib import admin

# Из модуля models импортируем модель Post
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    # Возможность изменять поле group в любом посте
    list_editable = ('group',)
    # Интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Возможность фильтрации по дате
    list_filter = ('pub_date',)
    # Свойство отображения пустых колонок
    empty_value_display = '-пусто-'


# При регистрации модели Post источником конфигурации для неё назначаем
# класс PostAdmin
admin.site.register(Post, Group, PostAdmin)
