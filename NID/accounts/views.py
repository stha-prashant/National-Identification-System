from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import UserRegisterForm, MyProfileForm, ApprovalForm

from accounts.models import *
from documents.models import *
from documents.views import get_nid_dict
from django.contrib.auth.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from accounts.profile import contacts

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
    return render(request, 'accounts/register.html', {
        'form': form,
        'title':'Register'
        })

def profileDetail(request):
    try:
        doc = Documents.objects.get(user=request.user)
        cit = doc.citizenship
        mydetailProfile = {
            'Full Name': f'{cit.first_name} {cit.middle_name or ""} {cit.last_name}',
            'Date of Birth': f'{cit.dob_bs} B.S.',
            'Gender': f'{cit.gender}',
            'Permanent Address':f'{cit.perma_region}, {cit.perma_district} District, {cit.perma_local}, Ward : {cit.perma_ward_no}',
            'Father\'s Name': f'{cit.father_first_name} {cit.father_middle_name or ""} {cit.father_last_name}',
            'Mother\'s Name':f'{cit.mother_first_name or ""} {cit.mother_middle_name or ""} {cit.mother_last_name or ""}',
            'Identity Number':f'{cit.citizenship_no}',
            'ID Issued Date':f'{cit.issue_date_bs}',
            'ID Issued From':f'{cit.perma_district} District'

        }
        return mydetailProfile
    except:
        raise ObjectDoesNotExist



@login_required
def profile(request):
    mycontacts  = contacts(request)
    try:
        mydetailProfile = profileDetail(request)
        context = {'title':'Profile',
                    'mydetails':mydetailProfile}
        context.update(mycontacts)
        return render(request, 'accounts/profile.html', context=context)
    except ObjectDoesNotExist:
        context = {'title':'Profile',
                    'message':'Please submit your documents first.'}
        context.update(mycontacts)
        return render(request, 'accounts/profile.html', context=context)


@login_required
def profile_update(request):
    mycontactDetails = contacts(request)

    # Just for comfirmation, contacts() call does the job.
    try:
        mycontact = MyPersonalDetail.objects.get(user=request.user)
        if request.method == 'POST':
            p_form = MyProfileForm(request.POST, request.FILES, instance=mycontact)
            if  p_form.is_valid():
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile-update')
        else:
            p_form = MyProfileForm(instance=mycontact)

        context = {
            'title':'Update Contacts',
            'form':p_form
        }

        context.update(mycontactDetails)
        return render(request, 'accounts/profile-update.html', context=context)
    except ObjectDoesNotExist:
        MyPersonalDetail(user=request.user).save()
        return redirect('profile-update')

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
    return render(request, 'accounts/profile-approval-request.html', {
        'form': form,
        'title':'Request'
        })

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
    return render(request, 'accounts/profile-approve.html', {
        'form': form,
        'title':'Approve'
        })

@login_required
def password_change(request):
    mycontacts  = contacts(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
        'title':'Change Password'
    }

    context.update(mycontacts)
    return render(request, 'accounts/change-password.html', context=context)


@login_required
def qrcode(request):
    try:
        documents = Documents.objects.get(user=request.user)
        national_id = documents.national_id
        if national_id:                            
            return render(request, 'documents/qrcode.html', {
                'national_id': json.dumps(get_nid_dict(documents), indent=4),
                'title': 'QR Code',
            })
        else:
            return render(request, 'documents/national_id.html', {
                'messages': ['Your citizenship has not been approved yet. Your National ID and the QR Code will be created automatically once an officer has approved your citizenship.', ],
                'title': 'QR Code',
            } )
    except:
        return render(request, 'accounts/qrcode.html',{
            'title':'QR Code'
        })

