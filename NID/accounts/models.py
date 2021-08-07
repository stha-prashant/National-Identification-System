from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from address.models import District
import uuid

# Create your models here.
class Officer(models.Model):
    # National ID is issued only by Home Ministry, so only they can verify your documents.
    officer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(User, on_delete=models.PROTECT, related_name="officerName")
    office = models.CharField(max_length=50)
    office_address = models.ForeignKey(District, null=False, on_delete=models.PROTECT)


    def __str__(self):
        return f"{self.account} working in {self.office}, District: {self.office_address}"

class Approval(models.Model):
    documentTypes=[
        ('CIT','Citizenship'),
        ('DRI', 'Driving License'),
        ('ELE', 'Voter Card')
    ]
    approval_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approval_type = models.CharField(max_length=3, choices=documentTypes, default='CIT')
    # Officers can be fired. If the referenced officer is fired, his/her work will still remain.
    approved_by = models.ForeignKey(Officer, null=False, on_delete=models.DO_NOTHING, related_name="approvingOfficer")

    def __str__(self):
        #ofcer = Officer.objects.get(officer_id = self.approved_by)
        doctType = {
        'CIT': 'Citizenship',
        'DRI': 'Driving License',
        'ELE' : 'Voter Card' }
        return f"{doctType[self.approval_type]}  approved by: {self.approved_by} "

# This if for testing purpose only