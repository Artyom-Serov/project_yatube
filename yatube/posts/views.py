from django.shortcuts import render


def index(request):
    # Передаем адрес шаблона в переменную
    template = 'posts/index.html'
    # Передаем строку для вывода из словаря
    title_index = 'Это главная страница проекта Yatube'
    text_index = 'Последние обновления на сайте.'
    context = {
        'title': title_index,
        'text': text_index
    }
    return render(request, template, context)


def group_posts(request):
    template = 'posts/group_list.html'
    title_group = 'Здесь будет информация о группах проекта Yatube'
    text_group = 'Лев Толстой – зеркало русской революции.'
    context = {
        'title': title_group,
        'text': text_group
    }
    return render(request, template, context)
