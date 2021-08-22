from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as account_view


urlpatterns = [
    path('register/', account_view.register, name='account-register'),
    path('profile/', account_view.profile, name='account-profile'),
    path('contacts/', account_view.profile_update, name='profile-update'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html',), name='account-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/index.html'), name='account-logout'),
    path('approve/citizenship/', account_view.approve, name='profile-approve'),
    path('approve/license/', account_view.approveLicense, name='license-approve'),
    path('password/', account_view.password_change, name='change-password'),
    path('qr/', account_view.qrcode, name='qrcode'),
    path('citzenship-deny/', account_view.denyApproval, name='deny-profile'),
    path('drivinglicense-deny/', account_view.denyLicense, name='deny-license'),
]
