from django.shortcuts import render, redirect
from django.views import View

from task_manager.users.models import User
from task_manager.users.forms import Register


class UsersView(View):
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, self.template_name, context={'users': users})


class UserRegister(View):
    template_name = 'user_create.html'

    def get(self, request, *args, **kwargs):
        form = Register
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(request, self.template_name, context={'form': form})


class UserEdit(View):
    template_name = 'user_edit.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = Register(instance=user)
        return render(request, self.template_name, context={'form': form, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = Register(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(request, self.template_name, context={'form': form, 'user_id': user_id})
