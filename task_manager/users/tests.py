from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import User


class UserTestCase(TestCase):
    fixtures = ['user.json', 'label.json', 'status.json', 'task.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.user_list = reverse('users')
        self.login = reverse('user_login')
        self.form_data = {
            'username': 'Aseliar',
            'last_name': 'Klevcov',
            'first_name': 'Pavel',
            'password1': 'qwerty1992',
            'password2': 'qwerty1992',
        }

    def test_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        response_task = list(response.context['user_list'])
        self.assertQuerysetEqual(response_task,
                                 [self.user1, self.user2, self.user3])

    def test_user_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_create.html')
        request = self.client.post(reverse('user_create'), self.form_data,
                                   follow=True)
        self.assertRedirects(request, reverse('user_login'))
        self.assertTrue(User.objects.get(pk=4))
        self.assertContains(request,
                            _('The user has been successfully registered'))

    def test_user_update(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('user_edit', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_edit.html')
        request = self.client.post(reverse('user_edit', args=[2]),
                                   self.form_data, follow=True)
        self.assertRedirects(request, reverse('users'))
        user = User.objects.get(pk=2)
        self.assertEqual(user.username, self.form_data['username'])
        self.assertContains(request,
                            _('User successfully changed'))

    def test_update_user_no_permission(self):
        self.client.force_login(self.user2)
        updated_user = reverse('user_edit', args=[1])
        """ GET """
        get_response = self.client.get(updated_user,
                                       follow=True)
        self.assertRedirects(get_response, self.user_list)
        """ POST """
        post_response = self.client.post(updated_user,
                                         self.form_data, follow=True)
        user1 = User.objects.get(id=1)
        self.assertRedirects(post_response, self.user_list)
        self.assertFalse(user1.username == self.form_data['username'])

    def delete_user_no_permission(self):
        self.client.force_login(self.user3)
        del_user1 = reverse('user_delete', args=[1])
        """ GET """
        get_response = self.client.get(del_user1)
        self.assertRedirects(get_response, self.user_list)
        self.assertEqual(len(User.objects.all()), 3)
        """ POST """
        post_response = self.client.post(del_user1, follow=True)
        self.assertContains(post_response,
                            _('You dont have the rights to change another user'))

    def delete_user_without_tasks(self):
        self.client.force_login(self.user3)
        del_user3 = reverse('user_delete', args=[3])
        """ GET """
        get_response = self.client.get(del_user3, follow=True)
        self.assertEqual(get_response.status_code, 200)
        """ POST """
        post_response = self.client.post(del_user3, follow=True)
        self.assertRedirects(post_response, self.user_list)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=3)
        self.assertContains(post_response, _('The user has been successfully deleted'))

    def delete_user_with_tasks(self):
        self.client.force_login(self.user2)
        del_user2 = reverse('user_delete', args=[2])
        """ GET """
        get_response = self.client.get(del_user2, follow=True)
        self.assertRedirects(get_response, self.user_list)
        self.assertEqual(len(User.objects.all()), 3)
        """ POST """
        post_response = self.client.post(del_user2, follow=True)
        self.assertContains(post_response, _('It is not possible to delete a user because it is being used'))

        # Create your tests here.
