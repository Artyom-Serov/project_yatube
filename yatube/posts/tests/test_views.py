from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
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
        self.author = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.author.username}):
                        'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.pk}):
                        'posts/post_detail.html',
            reverse('posts:create_post'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.pk}):
                        'posts/update_post.html',
            reverse('posts:add_comment',
                    kwargs={'post_id': self.post.pk}):
                        'posts/post_comment.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным словарем."""
        url = reverse('posts:index')
        response = self.guest_client.get(url)
        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 200)
        # Проверяем, что словарь передается в шаблон index.html
        self.assertTemplateUsed(response, 'posts/index.html')
        # содержит ли ответ с запрошенного URL-адреса текст,
        # сохраненный в посте
        self.assertContains(response, self.post.text)
        # содержит ли созданный слловарь переменную с именем 'page_obj'.
        self.assertIn('page_obj', response.context)
        # проверяем что словарь передает список записей в шаблон
        self.assertTrue(isinstance(
            response.context['page_obj'].object_list, list))
        self.assertTrue(len(response.context['page_obj'].object_list) > 0)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным словарем."""
        url = reverse('posts:group_list', kwargs={'slug': self.group.slug})
        response = self.guest_client.get(url)
        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 200)
        # Проверяем, что словарь передается в шаблон group_list.html
        self.assertTemplateUsed(response, 'posts/group_list.html')
        self.assertEqual(response.context['page_obj'][0], self.post)
        self.assertEqual(response.context['group'], self.group)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным словарем."""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': PostPagesTests.user.username})
        )
        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 200)
        # Проверяем, что словарь передается в шаблон profile.html
        self.assertTemplateUsed(response, 'posts/profile.html')
        self.assertIn(PostPagesTests.post, response.context['page_obj'])

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным словарем,
        фильтрация постов по id."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': PostPagesTests.post.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Тестовое описание текста')
        self.assertContains(response, self.post.author.username)
        self.assertContains(response, self.post.text)
        self.assertContains(response, self.post.group.title)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным словарем"""
        response = self.authorized_client.get(reverse('posts:create_post'))
        self.assertEqual(response.status_code, 200)
        context = response.context
        # Проверяем, что форма из контекста имеет нужные поля
        self.assertIn('form', context)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for field, field_class in form_fields.items():
            with self.subTest(field=field):
                self.assertIsInstance(
                    context['form'].fields[field], field_class)

    def test_post_create_show_correct_form(self):
        """Проверка правильности формы создания поста."""
        # Создаем словарь с данными формы
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        # Отправляем POST-запрос на создание поста
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True,
        )
        # Проверяем, что пост создан и
        # переход на страницу с постом произошел успешно
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, form_data['text'])
        self.assertContains(response, self.group.title)
        # Проверяем, что новый пост был добавлен в базу данных
        post = Post.objects.first()
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, self.group.id)
        self.assertEqual(post.author, self.user)
        # Проверяем, что новый пост был добавлен
        # в список постов на странице группы
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )
        self.assertContains(response, form_data['text'])

    def test_new_post_appears_on_index_page(self):
        """Новый пост появляется на главной странице."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertContains(response, self.post.text)

    def test_new_post_appears_on_group_page(self):
        """Новый пост появляется на странице группы."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        self.assertContains(response, self.post.text)
