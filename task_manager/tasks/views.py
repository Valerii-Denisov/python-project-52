from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.tasks.forms import Create
from task_manager.tasks.models import Task
from .filter import TaskFilter


class TaskView(LoginRequiredMixin, FilterView):
    template_name = 'tasks.html'
    model = Task
    context_object_name = 'tasks_list'
    login_url = reverse_lazy('user_login')
    filterset_class = TaskFilter

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request,
                         _('You are not logged in! Please log in')
                         )
        return redirect(url)


class TaskRegister(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'task_create.html'
    model = Task
    form_class = Create
    success_url = reverse_lazy('tasks')
    success_message = _('The tasks has been successfully registered')
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request,
                         _('You are not logged in! Please log in')
                         )
        return redirect(url)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'task_edit.html'
    model = Task
    form_class = Create
    success_url = reverse_lazy('tasks')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The task has been successfully updated')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request,
                         _('You are not logged in! Please log in')
                         )
        return redirect(url)


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,
                 DeleteView
                 ):
    template_name = 'task_delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The task has been successfully deleted')

    def test_func(self):
        task = self.get_object()
        return self.request.user.id == task.author.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message = _(
                'You dont have the rights to delete task of another user'
                )
            url = reverse_lazy('tasks')
        else:
            message = _('You are not logged in! Please log in')
            url = self.login_url
        messages.warning(self.request, message)
        return redirect(url)


class OneTaskView(LoginRequiredMixin, DetailView):
    template_name = 'task_detail.html'
    model = Task
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request,
                         _('You are not logged in! Please log in')
                         )
        return redirect(url)
