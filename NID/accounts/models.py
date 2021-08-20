from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

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
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_by')
    email = models.EmailField(verbose_name='Email', null=True)
    phone = PhoneNumberField(verbose_name='Phone Number', null=True, blank= True, unique=True)


    def __str__(self):
        return f"Approval Request Email {self.email} by {self.posted_by.username}"


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
    approved_document = models.OneToOneField(MyPersonalDetail, on_delete=models.CASCADE, related_name="ApprovalNumber")

    def __str__(self):
        doctType = {
        'CIT': 'Citizenship',
        'DRI': 'Driving License',
        'ELE' : 'Voter Card' }
        return f"{doctType[self.approval_type]}  approved by: {self.approved_by.account} "

#Note: There can be a document without approval number but there can't be an approval without a document. 
# This rule is voilated here. Rectify later on!