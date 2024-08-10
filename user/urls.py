from django.urls import path

from .views import UserRegisterApiView, UserLoginApiView, UserProfileApiView, UserLogoutApiView


urlpatterns = [
    path("register/", view=UserRegisterApiView.as_view(), name="user_register"),
    path("login/", view=UserLoginApiView.as_view(), name="user_login"),
    path("logout/", view=UserLogoutApiView.as_view(), name="user_logout"),
    path("profile/", view=UserProfileApiView.as_view(), name="user_profile"),
]