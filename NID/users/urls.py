from django.urls import path

from users import views as user_view

urlpatterns = [
    path("", user_view.index, name="user-index"),
    path("login", user_view.login_view, name="login"),
    path("logout", user_view.logout_view, name="logout")
]
