from django.forms import ModelForm
from .models import Status


class Create(ModelForm):

    class Meta:
        model = Status
        fields = (
            'name',
        )
