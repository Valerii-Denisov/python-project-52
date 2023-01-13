from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from task_manager.users.models import User
from task_manager.users.forms import Register


class UsersView(ListView):
    template_name = 'users.html'
    model = User
    context_object_name = 'user_list'


class UserRegister(SuccessMessageMixin, CreateView):
    template_name = 'user_create.html'
    model = User
    form_class = Register
    success_url = reverse_lazy('user_login')
    success_message = _('The user has been successfully registered')


class UserEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'user_edit.html'
    model = User
    form_class = Register
    success_url = reverse_lazy('users')
    pk_url_kwarg = 'id'
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

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        messages.success(self.request, _('User successfully changed'))
        return redirect(self.success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['user_id'] = user_id
        return context


class UserDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    template_name = 'user_delete.html'
    model = User
    success_url = reverse_lazy('users')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The user has been successfully deleted')

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
