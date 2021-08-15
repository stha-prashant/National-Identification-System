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

# Create your views here.
@login_required
def citizenship(request):
    try:
        documents = Documents.objects.get(user=request.user)
        citizenship = documents.citizenship
        return render(request, 'documents/citizenship.html', {
            'citizenship': citizenship
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
                'messages': ["Invalid form inputs! Please fix the following errors.",]
            })

    else:
        form = CitizenshipForm()
        return render(request, 'documents/citizenship.html', {
            'form': form
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
                'driving_license': driving_license
            })
    except Documents.DoesNotExist:
        return render(request, 'documents/driving_license.html', {
            'messages': ['Please submit your citizenship first', ]
        })
    

@method_decorator(login_required, name='dispatch')
class DrivingLicenseCreateView(CreateView):
    model = DrivingLicense
    fields = ['id', 'issue_date', 'issue_centre', 'blood_group', 'license_category', 'document_photo']
    template_name = "documents/driving_license.html"
    success_url = reverse_lazy('driving_license')