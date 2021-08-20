from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import *
from accounts.forms import UserRegisterForm, MyProfileForm, ApprovalForm


def contacts(request):
    try:
        mycontact = MyPersonalDetail.objects.get(user=request.user)
        mycontactDetail = {
            'phone': f'{mycontact.phone or ""}',
            'email': f'{mycontact.email or ""}',
            'image': f'{mycontact.profilePicture.url}'

        }
        return mycontactDetail
    except ObjectDoesNotExist:
        MyPersonalDetail(user=request.user).save()
        mycontactDetail={}
        return mycontactDetail