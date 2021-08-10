from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ajax/load_regions", views.load_regions, name='ajax_load_regions'),
    path("ajax/load_districts", views.load_districts, name="ajax_load_districts"),
    path("ajax/load_locals", views.load_locals, name="ajax_load_locals")
]