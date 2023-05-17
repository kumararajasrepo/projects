from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm


class AccountCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "email",
            "image",
            "username",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
