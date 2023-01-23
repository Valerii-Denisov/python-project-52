from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLogin(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'user_login.html'
    success_message = _('You are logged in')


class UserLogout(SuccessMessageMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)