from django.db import models
from django.core.exceptions import ValidationError#, ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db.models.signals import m2m_changed

# Create your models here.
class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    new_old = models.BooleanField(null=False)

    def __str__(self):
        if self.new_old:
            return f"{self.name} (Province)"
        else:
            return f"{self.name} (Zone)"

class District(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    new_old = models.BooleanField(null=True)
    region = models.ManyToManyField(Region, blank=False, related_name="districts")

    def clean(self):
        if self.new_old:
            try:
                self.region.get(new_old=self.new_old)
            except:
                # DoesNotExist or more than one exist exception raised
                raise ValidationError("District's new_old and region's new_old mismatch")

    def __str__(self):
        return f"{self.name}"


# def district_region_updated(sender, **kwargs):
#     kwargs["instance"].clean()

# m2m_changed.connect(district_region_updated, sender=District.region.through)



class LocalBodyCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    text_info = models.CharField(max_length=64, blank=False)
    new_old = models.BooleanField(null=True)
    
    def __str__(self):
        return f"{self.text_info}"

class LocalBody(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name=models.CharField(max_length=64, blank=False)
    num_wards = models.PositiveIntegerField(validators=[MinValueValidator(1),])
    new_old = models.BooleanField(null=False)
    category = models.ForeignKey(LocalBodyCategory, on_delete=models.PROTECT, related_name="local_bodies")
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="local_bodies")

    def clean(self):
        if self.category.new_old and self.category.new_old != self.new_old:
            raise ValidationError(f"Local body's new_old ({self.new_old}) and local body's category's new_old, ({self.category.new_old}) mismatch")
        if self.district.new_old and self.district.new_old != self.new_old:
            raise ValidationError(f"Local body's new_old, ({self.new_old}) and district's new_old, ({self.district.new_old}) mismatch")

    def __str__(self):
        return f"{self.name} {self.category}"


    
    

    

