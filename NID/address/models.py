from django.db import models

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
    new_old = models.BooleanField(null=False)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="districts")

    def __str__(self):
        return f"{self.name}"

class LocalBodyCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    text_info = models.CharField(max_length=64, blank=False)
    
    def __str__(self):
        return f"{self.text_info}"

class LocalBody(models.Model):
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=64, blank=False)
    new_old = models.BooleanField(null=False)
    category = models.ForeignKey(LocalBodyCategory, on_delete=models.PROTECT, related_name="local_bodies")
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="local_bodies")

    def __str__(self):
        return f"{self.name} {self.category}"
    

    

