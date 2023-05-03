from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Импортируем модель, чтобы обратиться к ней
from .models import Post, Group, User
from .forms import PostForm

DISPLAY = 10
# Количество отображаемых постов


def get_paginator(queryset, display, page_number):
    # функция для паджинации данных в шаблонах
    paginator = Paginator(queryset, display)
    page_obj = paginator.get_page(page_number)
    return paginator, page_obj


def index(request):
    # Передаем адрес шаблона в переменную
    template = 'posts/index.html'
    # В переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по ordering в классе Meta
    posts = Post.objects.all()
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Подключаем функцию паджинации
    paginator, page_obj = get_paginator(posts, DISPLAY, page_number)
    # Отдаем в словаре контекста для отправки информации в шаблон
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page')
    # Подключаем функцию паджинации
    paginator, page_obj = get_paginator(posts, DISPLAY, page_number)
    context = {
        'group': group,
        'posts': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user = get_object_or_404(User, username=username)
    post_list = user.post_set.all().order_by('-pub_date')
    page_number = request.GET.get('page')
    # Подключаем функцию паджинации
    paginator, page_obj = get_paginator(post_list, DISPLAY, page_number)
    context = {
        'author': user,
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    title = (f'Пост: {post.text[:30]}')
    context = {
        'post': post,
        'title': title,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.id)
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    is_edit = True
    return render(request, 'posts/update_post.html',
                  {'form': form, 'is_edit': is_edit}
                  )
