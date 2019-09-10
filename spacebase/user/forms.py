from django.forms import ModelForm
from localflavor.generic.forms import IBANFormField

from user.models import User


class UserForm(ModelForm):
    iban = IBANFormField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'iban']
