from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.statuses.models import Status
from task_manager.statuses.forms import Create
from task_manager.utils import DeleteFormValidMixin, HandelNoPermissionMixin


class StatusView(HandelNoPermissionMixin, ListView):
    """
    This class is responsible for displaying the list of status.
    """
    template_name = 'statuses/statuses.html'
    model = Status
    context_object_name = 'statuses_list'


class StatusRegister(HandelNoPermissionMixin, SuccessMessageMixin, CreateView):
    """
    This class is responsible for displaying the new status create page.
    """
    template_name = 'CRUD/create_update.html'
    model = Status
    form_class = Create
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully registered')
    extra_context = {'header': _('Create status'), 'button_name': _('Create')}


class StatusEdit(HandelNoPermissionMixin, SuccessMessageMixin, UpdateView):
    """
    This class is responsible for displaying the status data modification page.
    """
    template_name = 'CRUD/create_update.html'
    model = Status
    form_class = Create
    success_url = reverse_lazy('statuses')
    pk_url_kwarg = 'id'
    success_message = _('The status has been successfully updated')
    extra_context = {'header': _('Edit status'), 'button_name': _('To change')}


class StatusDelete(HandelNoPermissionMixin, DeleteFormValidMixin, DeleteView):
    """
    This class is responsible for displaying the status deletion page.
    """
    template_name = 'CRUD/delete.html'
    model = Status
    pk_url_kwarg = 'id'
    extra_context = {'header': _('Deleting a status')}
