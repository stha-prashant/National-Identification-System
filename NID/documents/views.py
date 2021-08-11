from django.shortcuts import render
from .forms import *
from documents.models import *
from address.models import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.
def citizenship(request):
    if request.method == 'POST':
        form = CitizenshipForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home-index"))
        else:
            return render(request, 'documents/citizenship.html', {
                'form': form,
                'message': "Invalid form inputs! Please fix the following errors."
            })

    else:
        form = CitizenshipForm()
        return render(request, 'documents/citizenship.html', {
            'form': form
        })


class DrivingLicenseCreateView(CreateView):
    model = DrivingLicense
    fields = ['id', 'issue_date', 'issue_centre', 'blod_group', 'license_category', 'document_photo']
    template_name = "documents/license.html"
    success_url = reverse_lazy('home-index')