from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages, auth
from django.views.decorators.http import require_POST
from requests import Session, session


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


def delete(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            request.user.delete()
            request.session.clear()
            return redirect("main")
    return render(request, "common/member_del.html")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            request.session.clear()
            messages.success(request, "Your password was successfully updated!")
            return redirect("main")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "common/change_password.html", {"form": form})


from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class PasswordResetView(auth_views.PasswordResetView):
    """
    비밀번호 초기화 - 사용자ID, email 입력
    """

    template_name = "common/password_reset.html"
    success_url = reverse_lazy("common:password_reset_done")
    email_template_name = "common/password_reset_email.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    비밀번호 초기화 - 메일 전송 완료
    """

    template_name = "common/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    비밀번호 초기화 - 새로운 비밀번호 입력
    """

    template_name = "common/password_reset_confirm.html"
    success_url = reverse_lazy("common:login")
