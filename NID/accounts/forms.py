from address.models import District, Region
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import MyPersonalDetail


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    # gives nested namespace for configuration and interacts with User model
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class MyProfileForm(forms.ModelForm):
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.EmailField(required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.all())

    class Meta:
        model = MyPersonalDetail
        fields = '__all__'

        