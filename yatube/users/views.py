
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView)
from django.urls import reverse_lazy
# Функция reverse_lazy позволяет получить URL по параметрам функции path().
from .forms import CreationForm
# Импортируем класс формы, чтобы сослаться на неё во view-классе


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


class PasswordChangeDoneView(TemplateView):
    template_name = 'users/password_change_done.html'


class PasswordReset(PasswordResetView):
    # Указываем шаблон для email
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'
    # Отключаем отправку email
    html_email_template_name = None
    # Отключаем отправку email
    from_email = None


class PasswordResetDoneView(TemplateView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'
