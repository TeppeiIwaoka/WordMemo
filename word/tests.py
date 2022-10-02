from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Word


class WordTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test_user',
        )
        self.word = Word.objects.create(
            word='test',
            part_of_speech='noun',
            definition='test definition',
            created_user=self.user
        )

    def test_redirect_if_user_logged_out(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

        response = self.client.get('/edit/1')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/delete/1')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_url_exists_at_correct_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/edit/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/delete/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

