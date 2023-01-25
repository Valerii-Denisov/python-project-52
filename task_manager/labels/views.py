from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.forms import Create
from task_manager.labels.models import Label


class LabelView(LoginRequiredMixin, ListView):
    """
    This class is responsible for displaying the list of label.
    """
    template_name = 'labels/labels.html'
    model = Label
    context_object_name = 'labels_list'
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)


class LabelRegister(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    This class is responsible for displaying the new label create page.
    """
    template_name = 'CRUD/create_update.html'
    model = Label
    form_class = Create
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('user_login')
    success_message = _('The label has been successfully registered')
    extra_context = {'header': _('Create label'), 'button_name': _('Create')}

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)


class LabelEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    This class is responsible for displaying the label data modification page.
    """
    template_name = 'CRUD/create_update.html'
    model = Label
    form_class = Create
    success_url = reverse_lazy('labels')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The label has been successfully updated')
    extra_context = {'header': _('Edit label'), 'button_name': _('To change')}

    def handle_no_permission(self):
        url = self.login_url
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)


class LabelDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    This class is responsible for displaying the label deletion page.
    """
    template_name = 'CRUD/delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    success_message = _('The label has been successfully deleted')
    extra_context = {'header': _('Deleting a label')}

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
                _('It is not possible to delete a label because it is being used'), # noqa
            )
            return redirect(self.success_url)
