from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import UserRegisterForm, MyProfileForm, ApprovalForm
from django.core import serializers
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.models import *
from documents.models import *
from documents.views import citizenship, driving_license, get_nid_dict
from django.contrib.auth.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from accounts.profile import contacts, profileDetail, get_national_ID, CitizenshipDetail, DrivingLicenseDetails

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

# Not a  good idea!
cit_id = 1

@login_required
def approve(request):
    off = Officer.objects.get(account=request.user.id)
    district = off.office_address
    cit = Citizenship.objects.filter(perma_district__id=district.pk, approval__isnull=True).first()

    context={
            'title':'Approval'
        }

    if cit is None:
        context={
            'notice':'No documents left for approval.',
            'title':'Approval'

        }
    else:
        #cit_data = serializers.serialize("json", cit)
        cit_data = CitizenshipDetail(cit)
        doc = Documents.objects.get(citizenship__id = cit.pk) # try?
        usr = doc.user.username
        documnt = doc.citizenship
        global cit_id
        cit_id = cit.pk
        #request.session['cit']=cit

        if request.method == 'POST':
            form = ApprovalForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                usrType = User.objects.get(username=request.user.username)
                form.instance.approved_by = Officer.objects.get(account=usrType)
                form.instance.approval_type = 'CIT'
                approve = form.save()
                cit.approval = approve
                cit.save()
                doc = Documents.objects.get(citizenship__id=cit.pk)
                doc.national_id = get_national_ID(district.pk) # try
                doc.save()
                messages.success(request, f'Citizenship Approved for {usr}')

                #license = doc.driving_license
                # if license:
                #     pass
                
                # else:
                return redirect('profile-approve')

        else:
            form = ApprovalForm()
        
        f={
            'form':form,
            'cit_data':cit_data,
            'username':usr,
            'document':documnt
        }

        context.update(f)
    return render(request, 'accounts/profile-approve.html', context = context)

@login_required
def denyApproval(request):
    global cit_id
    citizenship = Citizenship.objects.get(id=cit_id)
    #doc = Documents.objects.get(citizenship__id =cit_id)
    citizenship.delete()
    #cit = request.session.get('cit')
    return HttpResponseRedirect(reverse('profile-approve'))

dri_id=1
@login_required
def approveLicense(request):
    off = Officer.objects.get(account=request.user.id)
    district = off.office_address
    doc = Documents.objects.filter(citizenship__perma_district__id=district.pk, citizenship__approval__isnull=False, driving_license__isnull=False).all()
    documnt = doc.exclude(user=request.user)
    document = documnt.filter(driving_license__approval__isnull=True).first()

    context={
        'title':'Approve'
    }

    if document is None:
        context={
            'notice':'No documents left for approval.'

        }
    else:
        #license_data = serializers.serialize("json", license)
        license = document.driving_license
        license_data = DrivingLicenseDetails(license)
        usr = document.user.username
        global dri_id
        dri_id = license.pk

        if request.method == 'POST':
            form = ApprovalForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                usrType = User.objects.get(username=request.user.username)
                form.instance.approved_by = Officer.objects.get(account=usrType)
                form.instance.approval_type = 'DRI'
                approve = form.save()
                license.approval = approve
                license.save()
                messages.success(request, f'License Approved')
                return redirect('license-approve')

        else:
            form = ApprovalForm()
        f={
            'form':form,
            'username':usr,
            'license':license,
            'license_data':license_data
            
        }
        context.update(f)
    return render(request, 'accounts/profile-approve.html', context = context)

@login_required
def denyLicense(request):
    global dri_id
    document = Documents.objects.get(driving_license__id=dri_id)
    document.driving_license = None
    document.save()
    license = DrivingLicense.objects.get(id=dri_id)
    license.delete()
    #cit = request.session.get('cit')
    return HttpResponseRedirect(reverse('license-approve'))

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
            return render(request, 'accounts/qrcode.html', {
                'national_id': json.dumps(get_nid_dict(documents), indent=4),
                'title': 'QR Code',
            })
        else:
            return render(request, 'documents/national_id.html', {
                'messages': ['Your citizenship has not been approved yet. Your National ID and the QR Code will be created automatically once an officer has approved your citizenship.', ],
                'title': 'National ID',
            } )
    except:
        return render(request, 'accounts/qrcode.html',{
            'title':'QR Code'
        })

