from django.conf import settings
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Импортируем модель, чтобы обратиться к ней
from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm


def get_paginator(queryset, display, page_number):
    # функция для паджинации данных в шаблонах
    paginator = Paginator(queryset, display)
    page_obj = paginator.get_page(page_number)
    return paginator, page_obj


def index(request):
    # функция главной страницы
    key_prefix = 'index_page'
    posts = cache.get(key_prefix)
    if not posts:
        posts = Post.objects.all()
        cache.set(key_prefix, posts, timeout=20)
    # Передаем адрес шаблона в переменную
    template = 'posts/index.html'
    # В переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по ordering в классе Meta
    posts = Post.objects.all()
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Подключаем функцию паджинации
    paginator, page_obj = get_paginator(
        posts,
        settings.DISPLAY,
        page_number
    )
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
    paginator, page_obj = get_paginator(
        posts,
        settings.DISPLAY,
        page_number
    )
    context = {
        'group': group,
        'posts': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


def profile(request, username):
    # функция отображения деталей профайла
    author = get_object_or_404(User, username=username)
    post_list = author.post_set.all().order_by('-created')
    page_number = request.GET.get('page')
    # Подключаем функцию паджинации
    paginator, page_obj = get_paginator(
        post_list,
        settings.DISPLAY,
        page_number
    )
    following = request.user.is_authenticated
    if following:
        following = author.following.filter(user=request.user).exists()
    template = 'posts/profile.html'
    context = {
        'author': author,
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    # функция отображения информациии о посте
    post = get_object_or_404(Post, pk=post_id)
    title = (f'Пост: {post.text[:30]}')
    image_url = post.image.url if post.image else None
    comments = post.comments.all()
    form = CommentForm()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'title': title,
        'image_url': image_url,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    # функция комментирования поста
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def post_create(request):
    # функция для создания поста
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            create_post = form.save(commit=False)
            create_post.author = request.user
            create_post.save()
            return redirect('posts:profile', create_post.author)
    else:
        form = PostForm()
        template = 'posts/create_post.html'
        context = {'form': form}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    # функция для редактирования поста
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.id)
    template = 'posts/create_post.html'
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, template, context)


@login_required
def follow_index(request):
    # Получаем список последних постов от авторов,
    # на которых подписан пользователь
    posts = Post.objects.filter(
        author__following__user=request.user)
    page_obj = get_paginator(posts, settings.DISPLAY, request)
    context = {'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


# ВАРИАНТ themasterid
@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    user_follower = get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    )
    user_follower.delete()
    return redirect('posts:profile', username)


# ВАРИАНТ СЕТИ

# @login_required
# def profile_follow(request, username):
#    # Подписаться на автора
#    # Находим пользователя, на которого хотим подписаться
#    author = get_object_or_404(User, username=username)
#    # Создаем запись Follow
#    Follow.objects.get_or_create(user=request.user, author=author)
#    return redirect('posts:profile', username=username)

# @login_required
# def profile_unfollow(request, username):
#    # Дизлайк, отписка
#    # Находим пользователя, на которого хотим подписаться
#    author = get_object_or_404(User, username=username)
#    # Создаем запись Follow
#    Follow.objects.get_or_create(user=request.user, author=author)
#    return redirect('posts:profile', username=username)


# ВАРИАНТ РУДЕНКО со stackoverflow

# @login_required
# def profile_follow(request, username):
#    # Подписаться на автора
#    author = get_object_or_404(User, username=username)
#    if author != request.user:
#        Follow.objects.create(
#            user=request.user,
#            author=author,
#        )
#    return redirect(
#        'posts:profile',
#        author.username
#    )

# @login_required
# def profile_unfollow(request, username):
#    # Отписаться
#    author = get_object_or_404(User, username=username)
#    Follow.objects.filter(
#        user=request.user,
#        author=author,
#    ).delete()
#    return redirect(
#        'posts:profile',
#        author.username
#    )
