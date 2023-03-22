from django.http import HttpResponse


def index(request):
    return HttpResponse('Приветствую тебя, искательприключений!')


def group_posts(request, slug):
    return HttpResponse('Ваш пост {slug}')
