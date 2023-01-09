from django.shortcuts import render
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
        model = User
        form = Register
        return render(request, self.template_name, context={'form': form})
