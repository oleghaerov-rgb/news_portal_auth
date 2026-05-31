from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import News


class NewsPortalTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            password='StrongPass123!',
            first_name='Ivan',
            last_name='Petrov',
            email='author@example.com',
        )
        self.other_user = User.objects.create_user(
            username='reader',
            password='StrongPass123!',
            email='reader@example.com',
        )
        self.news = News.objects.create(
            title='Большая городская новость',
            summary='Краткое описание городской новости',
            content='Подробный текст новости с достаточным количеством символов.',
            author=self.author,
        )

    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'new_user',
                'first_name': 'Anna',
                'last_name': 'Ivanova',
                'email': 'anna@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='new_user').exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username='new_user').id)

    def test_news_create_requires_login(self):
        response = self.client.get(reverse('news_create'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('news_create')}")

    def test_logged_in_user_creates_news_as_author(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('news_create'),
            {
                'title': 'Новая важная публикация',
                'summary': 'Короткое описание новой публикации',
                'content': 'Полный текст новой публикации с достаточным количеством символов.',
            },
        )

        created_news = News.objects.get(title='Новая важная публикация')
        self.assertEqual(created_news.author, self.author)
        self.assertRedirects(response, reverse('news_detail', args=[created_news.id]))

    def test_only_author_can_edit_news(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('news_edit', args=[self.news.id]),
            {
                'title': 'Чужое изменение',
                'summary': 'Чужое описание новости',
                'content': 'Чужой текст новости с достаточным количеством символов.',
            },
        )

        self.assertEqual(response.status_code, 403)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, 'Большая городская новость')

    def test_only_author_can_delete_news(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse('news_delete', args=[self.news.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(News.objects.filter(id=self.news.id).exists())
