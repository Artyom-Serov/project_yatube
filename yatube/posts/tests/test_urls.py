from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='auth')
        # Создаем тестовую группу
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        # Создаем тестовый пост
        cls.post = Post.objects.create(
            text='Тестовое описание текста',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        # Создаём экземпляры клиента.
        self.guest_client = Client()
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls_uses_template_for_autorized(self):
        """Проверка запросов для авторизованных пользователей."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/update_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_template_for_non_autorized(self):
        """Проверка запросов для неавторизованных пользователей."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_nonexistent_page(self):
        """Проверка запросов не существуюшей
        страницы для любых пользователей.
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # Проверяем редиректы для неавторизованного пользователя
    def test_create_post_url_redirect_anonymous_on_login(self):
        """Страница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_post_edit_url_redirect_anonymous_on_login(self):
        """Страница по адресу /posts/<post_id>/edit/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(f'/posts/{self.post.pk}/edit/',
                                         follow=True)
        self.assertRedirects(
            response, (f'/auth/login/?next=/posts/{self.post.pk}/edit/'))
