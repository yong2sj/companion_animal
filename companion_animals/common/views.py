from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import UserForm, ProfileUpdateForm, ProfileForm, UserUpdateForm


def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        # 사용자가 입력한 폼 가져오기
        form = UserForm(request.POST)
        if form.is_valid():
            # db 반영
            form.save()
            # 로그인 페이지를 보여줄 때
            # return redirect('common:login')

            # form.cleaned_data.get() : 넘어온 폼에서 화면의 입력 값을 얻기 위한 함수
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            # authenticate() : 사용자 아이디와 비밀번호를 담아서 자격증명을 요청하는 함수
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                # login() : 로그인 해주는 함수
                login(request, user)

            # messages.success(request, f"Paws & Tails의 가족이 되신 걸 환영합니다!")
            return redirect("board:index")

    else:
        form = UserForm()

    return render(request, "common/signup.html", {"form": form})


@login_required
def profile(request):
    profile = Profile.objects.get(user_id=request.user)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f"계정이 업데이트 되었습니다!")
            return redirect("main")  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form, "profile": profile}

    return render(request, "common/profile.html", context)
