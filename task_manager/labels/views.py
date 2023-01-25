from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.forms import Create
from task_manager.labels.models import Label
from task_manager.utils import DeleteFormValidMixin, HandelNoPermissionMixin


class LabelView(HandelNoPermissionMixin, ListView):
    """
    This class is responsible for displaying the list of label.
    """
    template_name = 'labels/labels.html'
    model = Label
    context_object_name = 'labels_list'


class LabelRegister(HandelNoPermissionMixin, SuccessMessageMixin, CreateView):
    """
    This class is responsible for displaying the new label create page.
    """
    template_name = 'CRUD/create_update.html'
    model = Label
    form_class = Create
    success_url = reverse_lazy('labels')
    success_message = _('The label has been successfully registered')
    extra_context = {'header': _('Create label'), 'button_name': _('Create')}


class LabelEdit(HandelNoPermissionMixin, SuccessMessageMixin, UpdateView):
    """
    This class is responsible for displaying the label data modification page.
    """
    template_name = 'CRUD/create_update.html'
    model = Label
    form_class = Create
    success_url = reverse_lazy('labels')
    pk_url_kwarg = 'id'
    success_message = _('The label has been successfully updated')
    extra_context = {'header': _('Edit label'), 'button_name': _('To change')}


class LabelDelete(HandelNoPermissionMixin, DeleteFormValidMixin, DeleteView):
    """
    This class is responsible for displaying the label deletion page.
    """
    template_name = 'CRUD/delete.html'
    model = Label
    pk_url_kwarg = 'id'
    extra_context = {'header': _('Deleting a label')}
