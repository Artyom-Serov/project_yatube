from django.urls import path
from . import views
app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index_reference'),
    # Страница сообществ
    path('group/', views.group_posts, name='group_reference'),
]
