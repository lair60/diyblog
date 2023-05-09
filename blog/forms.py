import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
		
class CreateNewUserForm(forms.Form):
    email_user = forms.EmailField(help_text='A valid email address, please.')