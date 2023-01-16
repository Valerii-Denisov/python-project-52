from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from task_manager.statuses.models import Status
from task_manager.statuses.forms import Create


class StatusView(LoginRequiredMixin, ListView):
    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses_list'
    login_url = reverse_lazy('user_login')


    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)


class StatusRegister(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status_create.html'
    model = Status
    form_class = Create
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully registered')
    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)