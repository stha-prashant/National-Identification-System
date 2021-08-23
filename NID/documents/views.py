from django.shortcuts import render
from .forms import *
from documents.models import *
from address.models import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from accounts.profile import contacts, CitizenshipDetail, DrivingLicenseDetails

# Create your views here.
@login_required
def citizenship(request):
    try:
        documents = Documents.objects.get(user=request.user)
        citizenship = documents.citizenship
        return render(request, 'documents/citizenship.html', {
            'citizenship': citizenship,
            'citizenship_detail': CitizenshipDetail(citizenship) ,
            'title':'Citizenship'
        })
    except Documents.DoesNotExist:
        return HttpResponseRedirect(reverse("citizenship_form"))

def driving_license(request):
    pass


@login_required
def citizenship_form(request):
    if request.method == 'POST':
        form = CitizenshipForm(request.POST, request.FILES)
        
        if form.is_valid():
            citizenship = form.save(commit=False)
            try:
                documents = Documents.objects.get(user=request.user)
                documents.citizenship = citizenship
                citizenship.save()
                documents.save()
            except Documents.DoesNotExist:
                citizenship.save()
                Documents(citizenship=citizenship, user=request.user).save()

            return HttpResponseRedirect(reverse("citizenship"))
        else:
            return render(request, 'documents/citizenship.html', {
                'form': form,
                'messages': ["Invalid form inputs! Please fix the following errors.",],
                'title':'Citizenship'
            })

    else:
        form = CitizenshipForm()
        return render(request, 'documents/citizenship.html', {
            'form': form,
            'title':'Citizenship'
        })

@login_required
def driving_license(request):
    try:
        documents = Documents.objects.get(user=request.user)
        driving_license = documents.driving_license
        if not driving_license:
            return HttpResponseRedirect(reverse("driving_license_form"))
        else:
            return render(request, 'documents/driving_license.html', {
                'driving_license_detail': DrivingLicenseDetails(driving_license),
                'driving_license_photo': driving_license.document_photo,
                'title':'Driving License'
            })
    except Documents.DoesNotExist:
        return render(request, 'documents/driving_license.html', {
            'messages': ['Please submit your citizenship first', ],
            'title':'Driving License'
        })
    
@method_decorator(login_required, name='dispatch')
class DrivingLicenseCreateView(CreateView):
    model = DrivingLicense
    fields = ['id', 'issue_date', 'issue_centre', 'blood_group', 'license_category', 'document_photo']
    template_name = "documents/driving_license.html"
    success_url = reverse_lazy('driving_license')

    def form_valid(self, form):
        self.object = form.save()
        documents  = Documents.objects.get(user=self.request.user)
        documents.driving_license = self.object
        documents.save()
        return super(DrivingLicenseCreateView, self).form_valid(form)


def get_nid_dict(documents):
    assert documents.national_id is not None
    citizenship = documents.citizenship
    driving_license = documents.driving_license
    nid_dict = {
        'National ID': str(documents.national_id),
        'Name': f'{citizenship.first_name} {citizenship.middle_name or ""} {citizenship.last_name}',
        'Address': f'{citizenship.birth_local}- {citizenship.birth_ward_no}, {citizenship.birth_district}',
        'Driving License': f'{driving_license or "-"}'
    }
    return nid_dict

@login_required
def national_id(request):
    mycontacts  = contacts(request)
    try:
        documents = Documents.objects.get(user=request.user)
        national_id = documents.national_id
        if national_id:
            context = {
                 'national_id': get_nid_dict(documents),
                'title': 'National ID',
            }
            context.update(mycontacts)
            return render(request, 'documents/national_id.html',context=context)
        else:
            context={
                'messages': ['Your citizenship has not been approved yet. Your National ID will be created automatically once an officer has approved your citizenship.', ],
                'title': 'National ID',
            }
            context.update(mycontacts)
            return render(request, 'documents/national_id.html', context=context)
    except Documents.DoesNotExist:
        context={
             'messages': ['Please submit your citizenship first', ],
            'title': 'National ID',

        }
        return render(request, 'documents/national_id.html',context=context)
        