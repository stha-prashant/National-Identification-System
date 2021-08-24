from django.contrib import admin
from .models import *

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'new_old')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province', 'zone')

class LocalBodyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'num_wards', 'category', 'district')

class LocalBodyCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'new_old')

# Register your models here.
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(LocalBodyCategory, LocalBodyCategoryAdmin)
admin.site.register(LocalBody, LocalBodyAdmin)