<<<<<<< HEAD
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.core.paginator import Paginator
from django.db.models import Q, Count
=======
from django.shortcuts import redirect, render, get_object_or_404
>>>>>>> 6e16982f3ae8a0867d48bd72bc2205601a6697fe
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Board
from ..forms import BoardForm

# 게시글 등록
@login_required(login_url="common:login")
def board_create(request):

    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            # 작성자 추가(현재 로그인 사용자 : "request.user")
            board.author = request.user
            board.save()
            return redirect("board:index")

    else:
        form = BoardForm()

    return render(request, "board/board_form.html", {"form": form})


# 게시글 수정(원본 내용 보여준 후 수정)
@login_required(login_url="common:login")
def board_modify(request, board_id):

    # board_id 값에 맞는 질문 찾아오기
    board = get_object_or_404(Board, pk=board_id)

    if request.user != board.author:
        messages.error(request, "수정할 권한이 없습니다.")
        return redirect("board:detail", board_id=board_id)

    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.nickname = request.user
            board.modify_date = timezone.now()
            board.save()

            return redirect("board:detail", board_id=board_id)
    else:
        form = BoardForm(instance=board)

    return render(request, "board/board_form.html", {"form": form})


# 게시글 삭제
@login_required(login_url="common:login")
def board_delete(request, board_id):

    # board_id 질문 찾아오기
    board = get_object_or_404(Board, pk=board_id)

    if request.user != board.nickname:
        messages.error(request, "삭제할 권한이 없습니다.")
        return redirect("board:detail", board_id=board_id)

    # 삭제
    board.delete()

    return redirect("board:index")
