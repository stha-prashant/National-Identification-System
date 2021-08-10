from django.forms import ModelForm
from documents.models import *
from address.models import *

#TODO: https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html Update form fields to contain query sets based on address fields in "post" request
class CitizenshipForm(ModelForm):
    class Meta:
        model = Citizenship
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_region'].queryset = Region.objects.none()
        self.fields['birth_district'].queryset = District.objects.none()
        self.fields['birth_local'].queryset = LocalBody.objects.none()

        self.fields['perma_region'].queryset = Region.objects.none()
        self.fields['perma_district'].queryset = District.objects.none()
        self.fields['perma_local'].queryset = LocalBody.objects.none()


# class DrivingLicenseForm(ModelForm):
#     class Meta:
#         model = DrivingLicense
#         fields = '_all__'
