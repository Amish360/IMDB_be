from django.urls import path

from .views import (
    CustomUserDetail,
    CustomUserList,
    get_user_profile,
    update_user_profile,
    user_login,
)

urlpatterns = [
    path("register/", CustomUserList.as_view(), name="user-list"),
    path("register/<int:pk>/", CustomUserDetail.as_view(), name="user-detail"),
    path("get_user_profile/", get_user_profile, name="get_user_profile"),
    path("update_user_profile/", update_user_profile, name="update_user_profile"),
    path("login/", user_login, name="user_login"),
]
