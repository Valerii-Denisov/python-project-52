from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError

from task_manager.labels.models import Label
from task_manager.labels.forms import Create


class LabelView(LoginRequiredMixin, ListView):
    template_name = 'labels.html'
    model = Label
    context_object_name = 'labels_list'
    login_url = reverse_lazy('user_login')


    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)


class LabelRegister(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'label_create.html'
    model = Label
    form_class = Create
    success_url = reverse_lazy('labels')
    success_message = _('The label has been successfully registered')
    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)

class LabelEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'label_edit.html'
    model = Label
    form_class = Create
    success_url = reverse_lazy('labels')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The label has been successfully updated')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)

class LabelDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'label_delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The label has been successfully deleted')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(self.request, _('You are not logged in! Please log in'))
        return redirect(url)


    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(self.request, _('It is not possible to delete a label because it is being used'))
            return redirect(self.success_url)