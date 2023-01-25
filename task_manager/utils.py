from django.db.models import ProtectedError
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

SUCCESS_MESSAGE = {
    'User': _('The user has been successfully deleted'),
    'Status': _('The status has been successfully deleted'),
    'Label': _('The label has been successfully deleted'),
}
URL_NAME = {
    'User': 'users',
    'Status': 'statuses',
    'Label': 'labels',
}
WARNING_MESSAGE = {
    'User': _('It is not possible to delete a user because it is being used'),
    'Status': _('It is not possible to delete a status because it is being used'),  # noqa:E501
    'Label': _('It is not possible to delete a label because it is being used'),
}


class DeleteFormValidMixin:
    def form_valid(self, form):
        try:
            model_name = (self.object.__class__.__name__)
            url = reverse_lazy(URL_NAME[model_name])
            self.object.delete()
            messages.success(self.request, SUCCESS_MESSAGE[model_name])
            return redirect(url)
        except ProtectedError:
            messages.warning(self.request, WARNING_MESSAGE[model_name])
            return redirect(url)


class HandelNoPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        url = reverse_lazy('user_login')
        messages.warning(
            self.request,
            _('You are not logged in! Please log in'),
        )
        return redirect(url)
