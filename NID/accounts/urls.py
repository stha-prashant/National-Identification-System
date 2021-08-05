from django.urls import path

from accounts import views as account_view

urlpatterns = [
    path("register/", account_view.register, name="account-register"),
]
