from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PaginatorViewsTest(TestCase):
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
        # Создаем тестовые посты
        cls.post_count = 13
        cls.posts = []
        for i in range(cls.post_count):
            post = Post.objects.create(
                text=f'Тестовое описание текста {i+1}',
                author=cls.user,
                group=cls.group
            )
            cls.posts.append(post)

    def setUp(self):
        # Создаём экземпляры клиента.
        self.guest_client = Client()
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_paginator_index_is_authorized(self):
        """Проверяем паджинацию страниц в index.html."""
        for page_number, expected_count in ((1, 10), (2, 3)):
            with self.subTest(page_number=page_number):
                response = self.authorized_client.get(
                    reverse('posts:index') + f'?page={page_number}')
                self.assertEqual(
                    len(response.context['page_obj'].object_list),
                    expected_count
                )

    def test_paginator_index_is_non_authorized(self):
        """Проверяем паджинацию страниц в index.html."""
        for page_number, expected_count in ((1, 10), (2, 3)):
            with self.subTest(page_number=page_number):
                response = self.guest_client.get(
                    reverse('posts:index') + f'?page={page_number}')
                self.assertEqual(
                    len(response.context['page_obj'].object_list),
                    expected_count
                )

    def test_paginator_group_list_is_authorized(self):
        """Проверяем паджинацию страниц в group_list.html."""
        for page_number, expected_count in ((1, 10), (2, 3)):
            with self.subTest(page_number=page_number):
                response = self.authorized_client.get(
                    reverse('posts:group_list',
                            kwargs={'slug': PaginatorViewsTest.group.slug})
                    + f'?page={page_number}')
                self.assertEqual(len(response.context['page_obj']),
                                 expected_count)

    def test_paginator_group_list_is_non_authorized(self):
        """Проверяем паджинацию страниц в group_list.html."""
        for page_number, expected_count in ((1, 10), (2, 3)):
            with self.subTest(page_number=page_number):
                response = self.guest_client.get(
                    reverse('posts:group_list',
                            kwargs={'slug': PaginatorViewsTest.group.slug})
                    + f'?page={page_number}')
                self.assertEqual(len(response.context['page_obj']),
                                 expected_count)

    def test_paginator_profile(self):
        """Проверяем паджинацию страниц в profile.html."""
        for page_number, expected_count in ((1, 10), (2, 3)):
            with self.subTest(page_number=page_number):
                response = self.authorized_client.get(
                    reverse('posts:profile',
                            kwargs={'username':
                                    PaginatorViewsTest.user.username})
                    + f'?page={page_number}')
                self.assertEqual(
                    len(response.context['page_obj'].object_list),
                    expected_count
                )
