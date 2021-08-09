from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


from .models import *
from .forms import AddressForm
    
def index(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return HttpResponse("Success")
        else:
            return render(request, "address/address_form.html", {
                "form": form
            })
    else:
        form = AddressForm()
        return render(request, "address/address_form.html", {
            'form': form
        })

def load_regions(request):
    new_old = request.GET.get("new_old")
    regions = Region.objects.filter(new_old=new_old)
    return render(request, 'address/region_dropdown_list_options.html', {
        'regions': regions
    })

def load_districts(request):
    region = request.GET.get("region")
    districts = District.objects.filter(zone=region) or District.objects.filter(province=region)
    return render(request, 'address/district_dropdown_list_options.html', {
        'districts': districts
    
    })

#to fix: add local category field in model and add filtering based on category to this view
def load_locals(request):
    district = request.GET.get("district")
    locals = LocalBody.objects.filter(district=district)
    return render(request, 'address/local_dropdown_list_options.html', {
        'locals': locals
    })