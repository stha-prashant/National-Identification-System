from django.shortcuts import render
from .forms import *
from documents.models import *
from address.models import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
import random
from django.forms.models import model_to_dict
# Create your views here.
@login_required
def citizenship(request):
    try:
        documents = Documents.objects.get(user=request.user)
        citizenship = documents.citizenship
        citizenship_form = CitizenshipForm(data=model_to_dict(documents.citizenship))
        return render(request, 'documents/citizenship.html', {
            'citizenship': citizenship,
            'citizenship_form': citizenship_form,
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
                # national_id = f"{datetime.datetime.now().strftime('%Y%m%d')}{citizenship.birth_district.id}"
                # while True:
                #     try:
                #         national_id += f"{random.randint(1, 9999)}"
                #         Documents.objects.get(national_id=national_id)
                #         break
                #     except Documents.DoesNotExist:
                #         pass
                # Documents(national_id=national_id, citizenship=citizenship).save()
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
                'driving_license_form': DrivingLicenseForm(data=model_to_dict(driving_license)),
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

@login_required
def national_id(request):
    try:
        documents = Documents.objects.get(user=request.user)
        national_id = documents.national_id
        if national_id:
            return render(request, 'documents/national_id.html', {
                'documents': documents,
                'title': 'National ID',
            })
        else:
            return render(request, 'documents/national_id.html', {
                'messages': ['Your citizenship has not been approved yet. Your National ID will be created automatically once an officer has approved your citizenship.', ],
                'title': 'National ID',
            } )
    except Documents.DoesNotExist:
        return render(request, 'documents/national_id.html', {
            'messages': ['Please submit your citizenship first', ],
            'title': 'National ID',
        })
        