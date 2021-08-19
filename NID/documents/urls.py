from django.urls import path
from . import views

urlpatterns = [
    path('citizenship', views.citizenship, name="citizenship"),
    path('driving-license', views.driving_license, name="driving_license"),
    path('citizenship-form', views.citizenship_form, name="citizenship_form"),
    path('driving-license-form', views.DrivingLicenseCreateView.as_view(), name="driving_license_form"),
    path('national_id', views.national_id, name="national_id"),
]