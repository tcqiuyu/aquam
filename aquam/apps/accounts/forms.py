from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"Username",
        error_messages={'required':'Username is empty'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u'Username',
            }
        ),
    )
    password=forms.CharField(
        required=True,
        label=u'Password',
        error_messages={'required':'Password is empty'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u'Password',
            }
        )
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'Username and password is required')
        else:
            cleaned_data=super(LoginForm, self).clean()