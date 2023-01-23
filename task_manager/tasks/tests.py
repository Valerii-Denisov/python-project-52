from django.utils.translation import gettext as _
from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.core.exceptions import ObjectDoesNotExist


class TestTasksWithoutAuth(TestCase):

    def setUp(self):
        self.login = reverse('user_login')
        self.urls = [reverse('tasks'),
                     reverse('task_create'),
                     reverse('task_destroy', args=[1]),
                     reverse('task_edit', args=[2]),
                     reverse('task_see', args=[2])]

    def test_no_auth(self):
        for u in self.urls:
            response = self.client.get(u)
            self.assertRedirects(response, self.login)


class TasksTestCase(TestCase):

    fixtures = ['status.json', 'user.json',
                'task.json', 'label.json']

    def setUp(self):
        self.login = reverse('user_login')
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.tasks = reverse('tasks')
        self.t1 = Task.objects.get(pk=1)
        self.delete_task = reverse('task_destroy', args=[3])
        self.form_data = {'name': 'one more task',
                          'status': 1,
                          'description': '111',
                          'executor': 2,
                          'label': [1, 2, 3]}

    def test_task_list(self):
        self.client.force_login(self.user1)
        self.t2 = Task.objects.get(pk=2)
        self.t3 = Task.objects.get(pk=3)
        """ GET """
        response = self.client.get(self.tasks)
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['tasks_list'])
        self.assertQuerysetEqual(response_tasks,
                                 [self.t1, self.t2, self.t3])

    def test_show_task(self):
        self.client.force_login(self.user1)
        self.show_task = reverse('task_see', args=[1])
        """ GET """
        response = self.client.get(self.show_task)
        self.assertEqual(response.status_code, 200)
        descriptions = response.context['task']
        self.assertQuerysetEqual([descriptions.name, descriptions.author,
                                  descriptions.executor,
                                  descriptions.description,
                                  descriptions.status,
                                  descriptions.timestamp],
                                 [self.t1.name, self.t1.author,
                                  self.t1.executor, self.t1.description,
                                  self.t1.status, self.t1.timestamp])

    def test_create_task(self):
        self.client.force_login(self.user1)
        self.create_task = reverse('task_create')
        """ GET """
        get_response = self.client.get(self.create_task)
        self.assertEqual(get_response.status_code, 200)
        """ POST """
        post_response = self.client.post(
            self.create_task,
            self.form_data,
            follow=True,
        )
        self.assertRedirects(post_response, self.tasks)
        new_task = Task.objects.get(name=self.form_data['name'])
        self.assertEqual(new_task.executor.id, self.user2.id)
        self.assertEqual(new_task.author.id, self.user1.id)
        self.assertContains(
            post_response,
            _('The tasks has been successfully registered'),
        )

    def test_update_task(self):
        self.client.force_login(self.user1)
        self.update_task = reverse('task_edit', args=[2])
        """ GET """
        get_response = self.client.get(self.update_task)
        self.assertEqual(get_response.status_code, 200)
        """ POST """
        post_response = self.client.post(self.update_task,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.tasks)
        self.assertEqual(Task.objects.get(pk=2).executor, self.user2)
        self.assertContains(
            post_response,
            _('The task has been successfully updated'),
        )

    def test_delete_self_task(self):
        self.client.force_login(self.user3)
        """ GET """
        get_response = self.client.get(self.delete_task)
        self.assertEqual(get_response.status_code, 200)
        """ POST """
        post_response = self.client.post(self.delete_task, follow=True)
        self.assertRedirects(post_response, self.tasks)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=7)
        self.assertContains(
            post_response,
            _('The task has been successfully deleted'),
        )

    def test_delete_not_self_task(self):
        self.client.force_login(self.user1)
        """ GET """
        get_response = self.client.get(self.delete_task)
        self.assertRedirects(get_response, self.tasks)
        """ POST """
        post_response = self.client.post(self.delete_task, follow=True)
        self.assertRedirects(post_response, self.tasks)
        self.assertEqual(len(Task.objects.all()), 3)

    def test_filter(self):
        self.client.force_login(self.user2)
        """ GET """
        content_type_form1 = f'{self.tasks}?status=1&executor=2&label='
        get_response = self.client.get(content_type_form1)
        tasks_list = get_response.context['tasks_list']
        self.assertEqual(len(tasks_list), 1)
        task = tasks_list[0]
        self.assertEqual(task.name, 'Тест')
        self.assertEqual(task.executor.id, 2)
        self.assertEqual(task.status.id, 1)
        """ GET (self tasks) """
        content_type_form2 = f'{self.tasks}?self_task=on'
        get_response2 = self.client.get(content_type_form2)
        tasks_list = get_response2.context['tasks_list']
        self.assertEqual(len(tasks_list), 2)
        task = tasks_list[1]
        self.assertEqual(task.name, 'Тест2')
        self.assertEqual(task.author.id, 2)
