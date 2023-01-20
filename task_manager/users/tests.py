from django.test import TestCase
from .models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class UserTestCase(TestCase):
    fixtures = [ 'label', 'status.JSON', 'task.JSON']
    def setUp(self):
        self.user2 = User.objects.get(pk=12)
        self.user3 = User.objects.get(pk=13)
        self.user_list = reverse('user_list')
        self.login = reverse('login')
        self.form_data = {
            'username': 'Aseliar',
            'last_name': 'Klevcov',
            'first_name': 'Pavel',
            'password1': 'qwerty1992',
            'password2': 'qwerty1992',
        }

    def test_user_list(self):
        response = self.client.get(reverse('user_list'))
        print(response)
        self.assertEqual(response.status_code, '200')
# Create your tests here.
