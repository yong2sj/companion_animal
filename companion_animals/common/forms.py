from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label="사용자이름", widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    email = forms.EmailField(
        label="이메일", widget=forms.EmailInput(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = User
        fields = ("username", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("nickname", "phone", "species", "pet_name", "image")

        # 에러 메세지가 보여질 때 라벨명이 field명을 이용하기 때문에
        # 영어로 나오는 부분을 원하는 한글로 변경
        labels = {
            "nickname": "별명",
            "phone": "핸드폰번호",
            "species": "반려동물 종류",
            "pet_name": "반려동물 이름",
            "image": "사진",
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("nickname", "phone", "species", "pet_name", "image")
        labels = {
            "nickname": "별명",
            "phone": "핸드폰번호",
            "species": "반려동물 종류",
            "pet_name": "반려동물 이름",
            "image": "사진",
        }


# from django.core.exceptions import ValidationError
# import django.contrib.auth.forms as auth_forms
# from django.contrib.auth.models import User


# class PasswordResetForm(auth_forms.PasswordResetForm):
#     username = auth_forms.UsernameField(label="사용자ID")  # CharField 대신 사용

#     # validation 절차:
#     # 1. username에 대응하는 User 인스턴스의 존재성 확인
#     # 2. username에 대응하는 email과 입력받은 email이 동일한지 확인

#     def clean_username(self):
#         data = self.cleaned_data["username"]
#         if not User.objects.filter(username=data).exists():
#             raise ValidationError("해당 사용자ID가 존재하지 않습니다.")

#         return data

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get("username")
#         email = cleaned_data.get("email")

#         if username and email:
#             if User.objects.get(username=username).email != email:
#                 raise ValidationError("사용자의 이메일 주소가 일치하지 않습니다")

#     def get_users(self, email=""):
#         active_users = User.objects.filter(
#             **{
#                 "username__iexact": self.cleaned_data["username"],
#                 "is_active": True,
#             }
#         )
#         return (u for u in active_users if u.has_usable_password())
