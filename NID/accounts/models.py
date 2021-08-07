from django.db import models
from django.contrib.auth.models import User

from address.models import District
import uuid

# Create your models here.
class Officer(models.Model):
    # What if we use username as the primary key? Afterall, one person can work at one CDO office only.
    # If he/she is transferred simply change the address field.
    # How will you assign officer_id?

    # National ID is issued only by Home Ministry so only they can verify your documents.
    officer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(User, on_delete=models.PROTECT, related_name="officerName")
    office = models.CharField(max_length=50)
    office_address = models.ForeignKey(District, null=False, on_delete=models.PROTECT)


    def __str__(self):
        return f"{self.account} working in {self.office}"


