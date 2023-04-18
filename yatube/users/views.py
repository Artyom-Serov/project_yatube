from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
# Функция reverse_lazy позволяет получить URL по параметрам функции path().
from .forms import CreationForm
# Импортируем класс формы, чтобы сослаться на неё во view-классе
from django.core.mail import send_mail


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'

    send_mail(
        'Cмена пароля',
        'Текст письма.',
        'from@example.com',  # Это поле "От кого"
        ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
    )


class PasswordChangeDoneView(TemplateView):
    template_name = 'users/password_change_done.html'


class PasswordResetView(PasswordResetView):
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'
