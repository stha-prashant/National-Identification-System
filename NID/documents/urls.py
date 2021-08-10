from django.urls import path
from . import views

urlpatterns = [
    path('citizenship', views.citizenship, name="citizenship_form"),
    path('license', views.DrivingLicenseCreateView.as_view(), name="license_form")
]