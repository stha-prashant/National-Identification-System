from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

from address.models import District
import uuid

# Create your models here.
class Officer(models.Model):
    account = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="officerName")
    office = models.CharField(max_length=50, verbose_name='myOffice')
    office_address = models.ForeignKey(District, null=False, on_delete=models.PROTECT, related_name="officeAddress")


    def __str__(self):
          return f"{self.account} working in {self.office}, District: {self.office_address}"

class MyPersonalDetail(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='user_detail')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Phone Number', null=True, blank= True, unique=True)
    profilePicture = models.ImageField(default='default.png', upload_to='accounts')


    def __str__(self):
        return f"Email: {self.email} Phone {self.phone} Username: {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profilePicture.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.profilePicture.path)

class Approval(models.Model):
    documentTypes=[
        ('CIT','Citizenship'),
        ('DRI', 'Driving License'),
        ('ELE', 'Voter Card')
    ]
    approval_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approval_type = models.CharField(max_length=3, choices=documentTypes, default='CIT')
    # Officers can be fired.
    approved_by = models.ForeignKey(Officer, null=False, on_delete=models.DO_NOTHING, related_name="approvingOfficer")

    def __str__(self):
        doctType = {
        'CIT': 'Citizenship',
        'DRI': 'Driving License',
        'ELE' : 'Voter Card' }
        return f"{doctType[self.approval_type]}  approved by: {self.approved_by.account} "

#Note: There can be a document without approval number but there can't be an approval without a document. 
# This rule is voilated here. Rectify later on!