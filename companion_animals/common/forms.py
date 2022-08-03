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
    email = forms.EmailField(label="이메일")

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
