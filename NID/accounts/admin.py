from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User




from accounts.models import Officer, Approval, MyPersonalDetail

# Register your models here.

admin.site.register(Officer)
admin.site.register(Approval)
admin.site.register(MyPersonalDetail)