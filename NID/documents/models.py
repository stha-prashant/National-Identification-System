from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from address.models import *

# Create your models here.
# class BloodGroup(models.Model):
#     id = models.IntegerField(primary_key=True)
#     blood_group = models.CharField(max_length=3)

#     def __str__(self):
#         return f'Group({self.blood_group})'
    

# class DrivingLicenseIssueCentre(models.Model):
#     centre_id = models.IntegerField(primary_key=True)
#     province_id =""
#     district_id =""
#     local_id = ""
#     name = models.CharField(max_length=65, null=False)

#     def __str__(self):
#         return f"Licence Issued from {self.name}"

# class LicenceCategory(models.Model):
#         id = models.IntegerField(primary_key=True, null=False)
#         symbol = models.CharField(max_length=2, null=False)
#         description = models.CharField(max_length=50, null=False)

#         def __str__(self):
#             return f"{self.symbol} : {self.description}"

# class DrivingLicense(models.Model):
#     id = models.IntegerField(primary_key=True)
#     issue_date = models.DateField(auto_now=False, auto_now_add=False)
#     issue_centre = models.ForeignKey(DrivingLicenseIssueCentre, on_delte=models.PROTECT)
#     license_type = ""

# class DocumentID(models.Model):
#     pass


class CitizenshipType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return f"Citizenship Type: {self.name}"

class CitizenshipAct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    
    def __str__(self):
        return f"Citizenship Act: {self.name}"

class Citizenship(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    #approval = models.ForeignKey(Approval, on_delete=models.PROTECT, null=True)
    #photo_front = models.FileField()
    #photo_back = models.FileField()
    first_name = models.CharField(max_length=32, blank=False)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=False)
    address_old_new = models.BooleanField(null=False)
    birth_region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="born_citizens")
    birth_district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="born_citizens")
    birth_local = models.ForeignKey(LocalBody, on_delete=models.PROTECT, related_name="born_citizens")
    birth_ward_no = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(33)])
    perma_old_new = models.BooleanField(null=False)
    perma_region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="perma_citizens")
    perma_district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="perma_citizens")
    perma_local = models.ForeignKey(LocalBody, on_delete=models.PROTECT, related_name="perma_citizens")
    birth_ward_no = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(33)])
    dob_bs = models.DateField()
    #dob_ad = models.DateField()

    #issue: citizenship through mother
    father_first_name = models.CharField(max_length=32, blank=False)
    father_middle_name = models.CharField(max_length=32, blank=True, null=True)
    father_last_name = models.CharField(max_length=32, blank=False)
    
    #Will this be a problem
    father_citizenship_id = models.IntegerField()#blank=True, null=True)
    
    #issue: citizenship through mother
    mother_first_name = models.CharField(max_length=32, blank=True, null=True)
    mother_middle_name = models.CharField(max_length=32, blank=True, null=True)
    mother_last_name = models.CharField(max_length=32, blank=True, null=True)
    
    #Will this be a problem
    mother_citizenship_id = models.IntegerField()#blank=True, null=True)

    #issue: need to consider marital status, added another field perhaps
    is_married = models.BooleanField(null=False)
    spouse_first_name = models.CharField(max_length=32, blank=True, null=True)
    spouse_middle_name = models.CharField(max_length=32, blank=True, null=True)
    spouse_last_name = models.CharField(max_length=32, blank=True, null=True)
    spouse_citizenship_id = models.IntegerField(blank=True, null=True)

    citizenship_type = models.ForeignKey(CitizenshipType, on_delete=models.PROTECT, related_name="citizenships")
    #face_photo = models.FileField()

    issue_date_bs = models.DateField()
    citizenship_act = models.ForeignKey(CitizenshipAct, on_delete=models.PROTECT, related_name="citizenships")