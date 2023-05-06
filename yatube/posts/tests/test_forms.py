import shutil
import tempfile

from posts.forms import PostForm
from posts.models import Post, Group
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

User = get_user_model()
# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Для сохранения media-файлов в тестах будет использоватьсяgs
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TetsUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Модуль shutil - библиотека Python с прекрасными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение,
        # изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем авторизованный клиент
        # self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_create_post_with_group(self):
        """Валидная форма создает запись в Post с группой."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'group': PostFormTests.group.id,
            'text': 'Текст тестового сообщения с группой'
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, что пост был создан, и его кол-во увеличилось на 1
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     args=[PostFormTests.user.username]))
        self.assertTrue(
            Post.objects.filter(
                text='Текст тестового сообщения с группой',
                group=PostFormTests.group.id,
                author=PostFormTests.user
            ).exists()
        )
        # Проверим, что ничего не упало и страница отдаёт код 200
        self.assertEqual(response.status_code, 200)

    def test_create_post_without_group(self):
        """Валидная форма создает запись в posts без группы."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст тестового сообщения без группы'
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, что пост был создан, и его кол-во увеличилось на 1
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     args=[PostFormTests.user.username]))
        self.assertTrue(
            Post.objects.filter(
                text='Текст тестового сообщения без группы',
                group=None,
                author=PostFormTests.user
            ).exists()
        )
        # Проверим, что ничего не упало и страница отдаёт код 200
        self.assertEqual(response.status_code, 200)

    def test_edit_text_post_form(self):
        """Валидная форма проверки редактирования содержания поста."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Измененный текст тестового поста с группой'
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data,
            follow=True
        )
        # Проверяем, что пост был изменен и его кол-во не изменилось
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     args=[PostFormTests.post.id]))
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group_id=form_data['group'],
                author=self.user).exists()
        )
        # проверяем, что форма не работает при вводе некорректных данных
        form_data = {
            'text': '',
            'group': ''
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertFormError(response, 'form', 'text', 'Обязательное поле.')
        # Проверим, что ничего не упало и страница отдаёт код 200
        self.assertEqual(response.status_code, 200)

    def test_edit_group_post_form(self):
        """Валидная форма проверки изменения группы поста."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'group': '',
            'text': 'Измененный текст тестового поста с группой'
        }
        url = reverse('posts:post_edit', args=[self.post.id])
        response = self.authorized_client.post(
            url,
            data=form_data,
            follow=True
        )
        # Проверяем, что пост был изменен и его кол-во не изменилось
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response,
                             reverse('posts:post_detail', args=[self.post.id]))
        self.assertTrue(
            Post.objects.filter(
                text='Измененный текст тестового поста с группой',
                group=None,
                author=self.user).exists()
        )
        # Проверим, что ничего не упало и страница отдаёт код 200
        self.assertEqual(response.status_code, 200)

    def test_post_form_widgets(self):
        """Проверяем, что все виджеты формы отображаются на странице."""
        form = PostForm()
        expected_widgets = {
            'text': forms.Textarea,
            'group': forms.Select,
            'image': forms.FileInput
        }
        for field_name, expected_widget in expected_widgets.items():
            self.assertIsInstance(
                form.fields[field_name].widget,
                expected_widget,
                f"Неправильный виджет для поля {field_name}."
            )

    def test_create_post_with_image(self):
        """Валидная форма создает запись в posts с изображением."""
        # Подготавливаем данные для передачи в форму
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response,
                             reverse('posts:post_detail', args=[self.post.id]))
        # Проверяем, что создалась запись с нашим слагом
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=self.group.id,
                image='posts/small.gif'
                ).exists()
        )
