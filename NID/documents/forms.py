from django.forms import ModelForm
from documents.models import *

class CitizenshipForm(ModelForm):
    class Meta:
        model = Citizenship
        fields = '__all__'

# class DrivingLicenseForm(ModelForm):
#     class Meta:
#         model = DrivingLicense
#         fields = '_all__'
