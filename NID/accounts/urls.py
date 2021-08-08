from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as account_view


urlpatterns = [
    path('register/', account_view.register, name='account-register'),
    path('profile/', account_view.profile, name='account-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='account-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='account-logout'),
    path('approval-request/', account_view.approvalRequest, name='profile-request')
]
