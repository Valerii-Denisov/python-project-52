from django.forms import ModelForm
from .models import Label


class Create(ModelForm):

    class Meta:
        model = Label
        fields = (
            'name',
        )
