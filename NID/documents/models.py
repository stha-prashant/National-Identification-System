from django.db import models

# Create your models here.
class BloodGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    blood_group = models.CharField(max_length=3)

    def __str__(self):
        return f'Group({self.blood_group})'
    

class DrivingLicenseIssueCentre(models.Model):
    centre_id = models.IntegerField(primary_key=True)
    province_id =""
    district_id =""
    local_id = ""
    name = models.CharField(max_length=65, null=False)

    def __str__(self):
        return f"Licence Issued from {self.name}"

class LicenceCategory(models.Model):
        id = models.models.IntegerField(primary_key=True, null=False)
        symbol = models.CharField(max_length=2, null=False)
        description = models.CharField(max_length=50, null=False)

        def __str__(self):
            return f"{self.symbol} : {self.description}"

class DrivingLicense(models.Model):
    id = models.IntegerField(primary_key=True)
    issue_date = models.DateField(auto_now=False, auto_now_add=False)
    issue_centre = models.ForeignKey(DrivingLicenseIssueCentre, on_delte=models.PROTECT)
    license_type = ""

class DocumentID(models.Model):
    pass
