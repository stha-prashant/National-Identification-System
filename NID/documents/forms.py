from django.forms import ModelForm, DateInput
from documents.models import *
from address.models import *

class CitizenshipForm(ModelForm):
    class Meta:
        model = Citizenship
        exclude = ('approval', )
        widgets = {
            'dob_bs': DateInput(attrs = {'class': 'datepicker'}),
            'issue_date_bs': DateInput(attrs = {'class': 'datepicker'})
        }


    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_region'].queryset = Region.objects.filter(new_old=False)
        self.fields['birth_district'].queryset = District.objects.none()
        self.fields['birth_local_category'].queryset = LocalBodyCategory.objects.none()
        self.fields['birth_local'].queryset = LocalBody.objects.none()

        self.fields['perma_region'].queryset = Region.objects.filter(new_old=False)
        self.fields['perma_district'].queryset = District.objects.none()
        self.fields['perma_local_category'].queryset = LocalBodyCategory.objects.none()
        self.fields['perma_local'].queryset = LocalBody.objects.none()

        # TODO: DRY principle: create a single function for all these stuff below
        if 'birth_region' in self.data:
            try:
                new_old = int(self.data.get('birth_new_old'))
                self.fields['birth_region'].queryset = Region.objects.filter(new_old=new_old)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass
            
        if 'perma_region' in self.data:
            try:
                new_old = int(self.data.get('birth_new_old'))
                self.fields['perma_region'].queryset = Region.objects.filter(new_old=new_old)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass

        if 'birth_district' in self.data:
            try:
                region = self.data.get('birth_region')
                self.fields['birth_district'].queryset = (District.objects.filter(zone=region) or District.objects.filter(province=region))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass
    
        if 'perma_district' in self.data:
            try:
                region = self.data.get('perma_region')
                self.fields['perma_district'].queryset = (District.objects.filter(zone=region) or District.objects.filter(province=region))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass

        if 'birth_local_category' in self.data:
            try:
                # district = self.data.get('birth_district')
                new_old = self.data.get('birth_new_old')
                new_old = False
                if (new_old == "on"):
                    new_old = True
                self.fields['birth_local_category'].queryset = LocalBodyCategory.objects.filter(new_old=new_old)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass

        if 'perma_local_category' in self.data:
            try:
                # district = self.data.get('birth_district')
                new_old = self.data.get('perma_new_old')
                new_old = False
                if (new_old == "on"):
                    new_old = True
                self.fields['perma_local_category'].queryset = LocalBodyCategory.objects.filter(new_old=new_old)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass
            
        if 'birth_local' in self.data:
            try:
                district = self.data.get('birth_district')
                local_category = self.data.get('birth_local_category')
                self.fields['birth_local'].queryset = District.objects.get(pk=district).local_bodies.filter(category=local_category)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass


        if 'perma_local' in self.data:
            try:
                district = self.data.get('perma_district')
                local_category = self.data.get('perma_local_category')
                self.fields['perma_local'].queryset = District.objects.get(pk=district).local_bodies.filter(category=local_category)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            #if it is an update request
            # TODO: don't know what to do yet
            pass


            