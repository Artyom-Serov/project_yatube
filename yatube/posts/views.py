from django.shortcuts import render, get_object_or_404
# Импортируем модель, чтобы обратиться к ней
from .models import Post, Group

DISPLAY = 10
# Количество отображаемых постов


def index(request):
    # Передаем адрес шаблона в переменную
    template = 'posts/index.html'
    # В переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по ordering в классе Meta
    posts = Post.objects.all()[:DISPLAY]
    # В словаре context отправляем информацию в шаблон
    context = {
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = group.posts.all()[:DISPLAY]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
