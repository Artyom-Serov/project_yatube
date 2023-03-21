from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница')


def group_posts(request, pk):
    return HttpResponse('Ваш пост {pk}'.format(pk=pk))
