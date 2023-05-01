from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AboutTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='auth')

        cls.templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }

    def setUp(self):
        # Создаём экземпляры клиента.
        self.guest_client = Client()
        self.user = User.objects.create_user(username='TestUser')

    def test_urls_uses_correct_template(self):
        """Проверка шаблонов для адресов author и tech."""
        for address, template in self.templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_author_page_show_correct(self):
        """Проверка доступности адреса about/author."""
        url = reverse('about:author')
        response = self.guest_client.get(url)
        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Проверяем, что запрос передается в шаблон author.html
        self.assertTemplateUsed(response, 'about/author.html')

    def test_technology_page_show_correct(self):
        """Проверка доступности адреса about/tech."""
        url = reverse('about:tech')
        response = self.guest_client.get(url)
        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Проверяем, что запрос передается в шаблон author.html
        self.assertTemplateUsed(response, 'about/tech.html')
