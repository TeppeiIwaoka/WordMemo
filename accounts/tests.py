from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SignUpPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_sigup_form(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'test_user',
                'age': 26,
                'password1': 'testpass123',
                'password2': 'testpass123',

            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, 'test_user')
        self.assertEqual(get_user_model().objects.all()[0].age, 26)
