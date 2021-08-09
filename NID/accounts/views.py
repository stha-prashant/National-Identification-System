from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegisterForm, MyProfileForm, ApprovalForm

from accounts.models import Officer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Accounted Created! You can login now {username}')
            return redirect('account-login')

    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    usrType = User.objects.get(username=request.user.username)
    try:
        # findOfficer = Officer.objects.get(account=usrType)
        usrType.officerName 
        role = "Officer"
        return render(request, 'accounts/profile-officer.html',{
            "role": role
        })
    except ObjectDoesNotExist:
        role = "Citizen"
        return render(request, 'accounts/profile-citizen.html',{ 
            "role": role
        })


@login_required
def approvalRequest(request):
    if request.method == 'POST':
        form = MyProfileForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.posted_by = request.user
            form.save()
            messages.success(request, f'Submitted your request.')
            return redirect('profile-request')
    else:
        form = MyProfileForm()
    return render(request, 'accounts/profile-approval-request.html', {'form': form})

# Needs retification, review later.
@login_required
def approve(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            usrType = User.objects.get(username=request.user.username)
            form.instance.approved_by = Officer.objects.get(account=usrType)
            form.save()
            messages.success(request, f'Request Approved')
            return redirect('profile-approve')    
    else:
        form = ApprovalForm()
    return render(request, 'accounts/profile-approve.html', {'form': form})