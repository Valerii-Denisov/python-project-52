from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.tasks.models import Task
from task_manager.tasks.forms import Create


class TaskView(LoginRequiredMixin, ListView):
    template_name = 'tasks.html'
    model = Task
    context_object_name = 'tasks_list'
    login_url = reverse_lazy('user_login')


    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)


class TaskRegister(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'task_create.html'
    model = Task
    fields = ['name',
            'description',
            'status',
            'executor',
              ]
    #form_class = Create
    success_url = reverse_lazy('tasks')
    success_message = _('The tasks has been successfully registered')
    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)

'''
class StatusEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'status_edit.html'
    model = Status
    form_class = Create
    success_url = reverse_lazy('statuses')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The status has been successfully updated')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)

class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'status_delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The status has been successfully deleted')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)'''
