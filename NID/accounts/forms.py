from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import MyPersonalDetail, Approval, Officer


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField(required=False)

    # gives nested namespace for configuration and interacts with User model
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
class MyProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    #Phone number    

    class Meta:
        model = MyPersonalDetail
        fields = ['email']


class ApprovalForm(forms.ModelForm):
       class Meta:
        model = Approval
        fields = ['approval_type','approved_document']