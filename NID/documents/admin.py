from django.contrib import admin
from .models import *

class CitizenshipAdmin(admin.ModelAdmin):
    list_display = ('citizenship_no', 'approval', 'first_name', 'last_name','birth_district', 'perma_district')

class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_id', 'citizenship', 'driving_license',)

class DrivingLicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'approval', 'license_category', 'blood_group', 'issue_date', 'issue_centre')

# Register your models here.
admin.site.register(CitizenshipAct)
admin.site.register(CitizenshipType)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(DrivingLicenseIssueCentre)
admin.site.register(DrivingLicense, DrivingLicenseAdmin)
admin.site.register(Documents, DocumentsAdmin)
