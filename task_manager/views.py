from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


class UserLogin(SuccessMessageMixin, LoginView):
    template_name = 'user_login.html'
    success_message = _('You are logged in')


class UserLogout(SuccessMessageMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)