from django.shortcuts import render
from task_manager.users.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    return render(request, 'index.html')


class UserLogin(SuccessMessageMixin, LoginView):
    template_name = 'user_login.html'
    success_message = "Ты в матрице"