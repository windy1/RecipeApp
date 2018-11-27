from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.models import UserProfile


class SignUpForm(UserCreationForm):
    """
    Form submitted when a users signs up for a new account

    See: templates/registration/signup.html template
    """

    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SaveUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('image', 'bio')


class SearchForm(forms.Form):
    q = forms.CharField(required=True)
