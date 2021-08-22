from django.core.exceptions import ObjectDoesNotExist
from accounts.models import *
from documents.models import Documents
import random
import datetime

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
            'ID Issued Date':f'{cit.issue_date_bs} B.S.',
            'ID Issued From':f'{cit.perma_district} District'

        }
        return mydetailProfile
    except:
        raise ObjectDoesNotExist


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



def get_national_ID(district):
    tday = datetime.date.today().day
    did = str(tday) + "-" + str(district)

    value = random.randint(1, 99999)
    value = str(value)
    length = len(value)

    if length < 5:
        value = (5-length)*str(0)+value

    nid = did+"-"+str(value)
    return nid


def CitizenshipDetail(cit):
    if cit is not None:
        citDetails= {
            'Citizenship No.:':f'{cit.citizenship_no}',
            'Full Name': f'{cit.first_name} {cit.middle_name or ""} {cit.last_name}',
            'Date of Birth': f'{cit.dob_bs} B.S.',
            'Gender': f'{cit.gender}',
            'Birth Address':f'{cit.birth_region}, {cit.birth_district} District, {cit.birth_local}, Ward : {cit.birth_ward_no}',
            'Permanent Address':f'{cit.perma_region}, {cit.perma_district} District, {cit.perma_local}, Ward : {cit.perma_ward_no}',
            'Father\'s Name': f'{cit.father_first_name} {cit.father_middle_name or ""} {cit.father_last_name}',
            'Father\'s Citizenship': f'{cit.father_citizenship_id}',
            'Mother\'s Name':f'{cit.mother_first_name or ""} {cit.mother_middle_name or ""} {cit.mother_last_name or ""}',
            'Mother\'s Citizenship': f'{cit.mother_citizenship_id}',
            'Spouse\'s Name':f'{cit.spouse_first_name or ""} {cit.spouse_middle_name or ""} {cit.spouse_last_name or ""}',
            'Spouse\'s Citizenship': f'{cit.spouse_citizenship_id or ""}',
            'Citizenship Act':f'{cit.citizenship_act}',
            'Citizenship Type': f'{cit.citizenship_type}',
            'ID Issued Date':f'{cit.issue_date_bs}',
            'ID Issued From':f'{cit.perma_district} District'
        }
        return citDetails
    else:
        citDetails={}
        return citDetails

def DrivingLicenseDetails(license):
    if license is not None:
        licenseDetails={
            'License Number:': f'{license.id}',
            'Issued Date:':f'{license.issue_date}',
            'Blood Group:':f'{license.blood_group}',
            'Category:': f'{license.license_category}',
            }
        return licenseDetails
    else:
        licenseDetails = {}
        return licenseDetails
  