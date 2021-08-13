from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from address.models import *
from accounts.models import Approval
from multiselectfield import MultiSelectField
from django.conf import settings

# Create your models here.
# issue with documents: for new creation documents id should be assigned not entered; solution: autofield for primary key, char field for document_no
# issue with license: 


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
    id = models.AutoField(primary_key=True)
    citizenship_no = models.CharField(max_length=64, blank=False, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    approval = models.ForeignKey(Approval, on_delete=models.PROTECT, null=True, blank=True, related_name="citizenships")
    photo_front = models.FileField(upload_to="citizenship/", blank=True, null=True)
    photo_back = models.FileField(upload_to="citizenship/", blank=True, null=True)
    first_name = models.CharField(max_length=32, blank=False)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=False)
    birth_new_old = models.BooleanField(null=False)
    birth_region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="born_citizens")
    birth_district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="born_citizens")
    birth_local_category = models.ForeignKey(LocalBodyCategory, on_delete=models.PROTECT, related_name="born_citizens")
    birth_local = models.ForeignKey(LocalBody, on_delete=models.PROTECT, related_name="born_citizens")
    birth_ward_no = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(33)])

    perma_new_old = models.BooleanField(null=False)
    perma_region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="perma_citizens")
    perma_district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="perma_citizens")
    perma_local_category = models.ForeignKey(LocalBodyCategory, on_delete=models.PROTECT, related_name="perma_citizens")
    perma_local = models.ForeignKey(LocalBody, on_delete=models.PROTECT, related_name="perma_citizens")
    perma_ward_no = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(33)])

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
    mother_citizenship_id = models.IntegerField(blank=True, null=True)

    #issue: need to consider marital status, added another field perhaps
    is_married = models.BooleanField(null=False)
    spouse_first_name = models.CharField(max_length=32, blank=True, null=True)
    spouse_middle_name = models.CharField(max_length=32, blank=True, null=True)
    spouse_last_name = models.CharField(max_length=32, blank=True, null=True)
    spouse_citizenship_id = models.IntegerField(blank=True, null=True)

    citizenship_type = models.ForeignKey(CitizenshipType, on_delete=models.PROTECT, related_name="citizenships")
    face_photo = models.FileField(upload_to="citizenship/", blank=True, null=True)

    issue_date_bs = models.DateField()
    citizenship_act = models.ForeignKey(CitizenshipAct, on_delete=models.PROTECT, related_name="citizenships")

    def __str__(self):
        return f"ID: {self.citizenship_no} from {self.birth_district.name}"
    
    
class DrivingLicenseIssueCentre(models.Model):
    centre_id = models.IntegerField(primary_key=True)
    province = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="license_issue_centers")
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="license_issue_centers")
    local = models.ForeignKey(LocalBody, on_delete=models.PROTECT, related_name="license_issue_centers") 
    name = models.CharField(max_length=65, blank=False, null=False)

    def __str__(self):
        return f"{self.name}, {self.district}"


class DrivingLicense(models.Model):
    LICENSE_CATEGORY_CHOICES=(
        ("A", "A: Motorycle, Scooter, Moped"),
        ("B", "B: Car, Jeep, Delivery Van"),
        ("K", "K: Scooter, Moped"),
        ("C", "C: Tempo, Auto Ricksaw"),
        ("C1", "C1: E-Rickshaw"),
        ("D", "D: Power Tiller"),
        ("E", "E: Tractor"),
        ("F", "F: Minibus, Minitruck"),
        ("G", "G: Truck, Bus, Lorry"),
        ("H", "H: Road Roller, Dozer"),
        ("H1", "H1:Dozer"),
        ("H2", "H2: Road Roller"),
        ("I", "I: Crane, Fire Brigade, Loader"),
        ("I1", "I1: Crane"),
        ("I2", "I2: Fire Brigade"),
        ("I3", "I3: Loader"),
        ("J1", "J1: Excavator"),
        ("J2", "J2: Backhoe Loader"),
        ("J3", "J3: Grader"),
        ("J4", "J4: Forklift"),
        ("J5", "J5: Other"),
    )
    BLOOD_GROUP_CHOICES=(
        ("A+", "A+"),
        ("B+", "B+"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )
    id = models.IntegerField(primary_key=True)
    issue_date = models.DateField(auto_now=False, auto_now_add=False)
    issue_centre = models.ForeignKey(DrivingLicenseIssueCentre, on_delete=models.PROTECT, blank=True, null=True, related_name="licenses")
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, max_length=3)
    license_category = MultiSelectField(choices=LICENSE_CATEGORY_CHOICES, max_length=32) 
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name="licenses", blank=True, null=True) 
    document_photo = models.FileField(upload_to="license/", blank=True, null=True)

    def __str__(self):
        return f"ID: {self.id}, Category(s): {self.license_category}"


class Documents(models.Model):
    citizenship = models.ForeignKey(Citizenship, on_delete=models.CASCADE, related_name="documents")
    driving_license = models.ForeignKey(DrivingLicense, on_delete=models.PROTECT, related_name="documents", blank=True, null=True)
    national_id = models.PositiveIntegerField(blank=True, null=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents")

    
