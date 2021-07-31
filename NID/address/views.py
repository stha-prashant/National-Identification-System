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