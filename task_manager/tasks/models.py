from django.db import models
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    description = models.TextField(null=True, verbose_name=_('Description'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_('Status'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Author'))
    executor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='executor', verbose_name=_('Executor'))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
