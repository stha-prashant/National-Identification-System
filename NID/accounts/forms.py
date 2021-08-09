from address.models import District, Region
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
    # Phone number    

    class Meta:
        model = MyPersonalDetail
        fields = ['email','usrname']


class ApprovalForm(forms.ModelForm):
    documentTypes=[
        ('CIT','Citizenship'),
        ('DRI', 'Driving License'),
        ('ELE', 'Voter Card')
        ]
    approval_type = forms.CharField(max_length=3)
    approved_by = forms.ModelChoiceField(queryset=Officer.objects.all())
    approved_document = forms.ModelChoiceField(queryset=MyPersonalDetail.objects.all())

    class Meta:
        model = Approval
        fields =['approval_type','approved_by','approved_document']
    