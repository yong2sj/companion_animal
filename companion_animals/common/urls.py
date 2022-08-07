from xml.etree.ElementInclude import include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "common"

urlpatterns = [
    # django.contrib.auth 에서 제공하는 LoginView
    # 클래스를 활용하기 때문에 별도의 views 는 작성하지 않음
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("member_del/", views.delete, name="delete"),
    path("change_password/", views.change_password, name="change_password"),
    # 비밀번호 초기화
    path(
        "password_reset/",
        views.PasswordResetView.as_view(template_name="common/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        views.PasswordResetDoneView.as_view(
            template_name="common/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="common/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
]
