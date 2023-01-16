from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from task_manager.statuses.models import Status
from task_manager.users.forms import Register


class StatusView(ListView):
    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses_list'
    login_url = reverse_lazy('user_login')


    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message = _('You dont have the rights to change another user')
            url = reverse_lazy('users')
        else:
            message = _('You are not logged in! Please log in')
            url = self.login_url
        messages.warning(self.request, message)
        return redirect(url)