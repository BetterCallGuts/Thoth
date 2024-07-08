from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from .models import models
from django import forms

class UserCustomForm(UserCreationForm):

    class Meta:
        model = User
        fields= ["username","email",  "password1", "password2"]
        "{{}}"

class SummitForm(forms.ModelForm):
    class Meta:
        model = models.SummitTicket
        fields = "__all__"