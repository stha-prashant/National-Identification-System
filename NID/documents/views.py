from django.shortcuts import render
from .forms import *
from documents.models import *
from address.models import *

# Create your views here.
def citizenship(request):
    if request.method == 'POST':
        return "form submitted"
    else:
        form = CitizenshipForm()
        return render(request, 'documents/citizenship.html', {
            'form': form
        })




# def license(request):
#     if request.method == 'POST':
#         return "form submitted"
#     else:
#         form = DrivingLicenseForm()
#         return render(request, 'documents/license.html', {
#             'form': form
#         })
