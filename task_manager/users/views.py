from django.shortcuts import render
from django.views import View

from task_manager.users.models import User


class UsersView(View):
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, self.template_name, context={'users': users})
