from django import forms
from django.contrib.auth.models import User

from users.models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', "password")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"