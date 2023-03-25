from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
    # Страница сообществ
    path('group/', views.group_posts),
]
