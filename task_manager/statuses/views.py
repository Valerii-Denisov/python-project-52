from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError

from task_manager.statuses.models import Status
from task_manager.statuses.forms import Create


class StatusView(LoginRequiredMixin, ListView):
    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses_list'
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)


class StatusRegister(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status_create.html'
    model = Status
    form_class = Create
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully registered')
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)


class StatusEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'status_edit.html'
    model = Status
    form_class = Create
    success_url = reverse_lazy('statuses')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The status has been successfully updated')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)


class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'status_delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The status has been successfully deleted')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(
                self.request,
                _('It is not possible to delete a status because it is being used'),# noqa
            )
            return redirect(self.success_url)
