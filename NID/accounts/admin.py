from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import Officer, Approval, MyPersonalDetail

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('account', 'office', 'office_address')

class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('approval_no', 'approval_type', 'approved_by')

class MyPersonalDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'profilePicture')

# Register your models here.

admin.site.register(Officer, OfficerAdmin)
admin.site.register(Approval, ApprovalAdmin)
admin.site.register(MyPersonalDetail, MyPersonalDetailAdmin)