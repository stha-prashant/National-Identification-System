from django.shortcuts import render
from .forms import *
from documents.models import *
from address.models import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Create your views here.
def citizenship(request):
    if request.method == 'POST':
        return "form submitted"
    else:
        form = CitizenshipForm()
        return render(request, 'documents/citizenship.html', {
            'form': form
        })


class DrivingLicenseCreateView(CreateView):
    model = DrivingLicense
    fields = "__all__"
    template_name = "documents/license.html"
    success_url = reverse_lazy('home-index')