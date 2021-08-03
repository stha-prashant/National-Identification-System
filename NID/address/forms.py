from django.core.exceptions import ValidationError
from django import forms
from .models import *

class AddressForm(forms.Form):
    #new_old = forms.MultipleChoiceField(choices=((True, 'New'), (False, 'Old')))
    new_old = forms.BooleanField(required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.all())
    local_body_category = forms.ModelChoiceField(queryset=LocalBodyCategory.objects.all())
    local_body = forms.ModelChoiceField(queryset=LocalBody.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        new_old = cleaned_data.get("new_old")
        region = cleaned_data.get("region")
        district = cleaned_data.get("district")
        local_body_category = cleaned_data.get("local_body_category")
        local_body = cleaned_data.get("local_body")

        if not new_old:
            new_old = False

        if region:
            if region.new_old != new_old:
                raise forms.ValidationError(f"Region's new_old, ({region.new_old}) doesn't match with form's new_old, ({new_old})")
        if district:
            if new_old:
                if (district.province != region):
                    raise ValidationError(f"District, {district} does not belong to specified province; {district.province} != {region}")
            else:
                if (district.zone != region):
                    raise ValidationError(f"District, {district} does  belong to specified zone; {district.zone} != {region}")
        if local_body_category and local_body:
            if (local_body.district != district):
                raise ValidationError(f"Local Body, {local_body} doesn't belong to specified district, {local_body.district}")
            if (local_body.category != local_body_category):
                raise ValidationError(f"Local Body {local_body} doesn't belong to specified category, {local_body_category}")