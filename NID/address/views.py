from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Q


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

def load_local_categories(request):
    # TODO: maybe add filtering based on district 
    # district = request.GET.get("district")
    new_old = request.GET.get("new_old")
    local_categories = LocalBodyCategory.objects.filter(Q(new_old=new_old) | Q(new_old=None)) 
    return render(request, 'address/local_category_dropdown_list_options.html', {
        'local_categories': local_categories
    })

def load_locals(request):
    district = request.GET.get("district")
    local_category = request.GET.get("local_category")
    locals = LocalBody.objects.filter(category=local_category, district=district)
    return render(request, 'address/local_dropdown_list_options.html', {
        'locals': locals
    })