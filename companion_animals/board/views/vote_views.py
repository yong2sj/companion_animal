from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Board


# 게시물 추천 등록
@login_required(login_url="common:login")
def vote_board(request, board_id):
    # board_id 해당하는 게시물 가져오기
    board = get_object_or_404(Board, pk=board_id)
    # 자신의 글은 추천 불가 로그인 사용자 == 질문작성자
    if request.user == board.nickname:
        messages.error(request, "본인이 작성한 글은 추천할 수 없습니다.")
    else:
        # board.voter + 1
        board.voter.add(request.user)
    return redirect("board:detail", board_id=board_id)
