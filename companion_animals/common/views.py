from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import UserForm


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
            return redirect("board:index")

    else:
        form = UserForm()

    return render(request, "common/signup.html", {"form": form})
