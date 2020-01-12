from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class LinkSubmitForm(forms.Form):

    general_link = forms.CharField(max_length=100)


class WordSearchForm(forms.Form):
    word = forms.CharField(max_length=100)
