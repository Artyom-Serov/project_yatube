from django.urls import reverse_lazy
"""Функция reverse_lazy позволяет получить URL
по параметрам функции path().
"""
from django.views.generic import CreateView
"""Импортируем CreateView, чтобы создать ему наследника."""
from .forms import CreationForm
"""Импортируем класс формы, чтобы сослаться на неё во view-классе."""


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
