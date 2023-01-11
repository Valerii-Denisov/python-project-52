from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.models import User
from task_manager.users.forms import Register


class UsersView(ListView):
    template_name = 'users.html'
    model = User
    context_object_name = 'user_list'


class UserRegister(CreateView):
    template_name = 'user_create.html'
    model = User
    form_class = Register
    success_url = reverse_lazy('users')


class UserEdit(UpdateView):
    template_name = 'user_edit.html'
    model = User
    form_class = Register
    success_url = reverse_lazy('users')
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['user_id'] = user_id
        return context


class UserDelete(DeleteView):
    template_name = 'user_delete.html'
    model = User
    success_url = reverse_lazy('users')
    pk_url_kwarg = 'id'
