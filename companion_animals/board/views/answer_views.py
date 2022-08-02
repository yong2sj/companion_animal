from django.shortcuts import redirect, render, get_object_or_404, resolve_url
<<<<<<< HEAD
from django.core.paginator import Paginator
from django.db.models import Q, Count
=======
>>>>>>> 6e16982f3ae8a0867d48bd72bc2205601a6697fe
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Board, Answer
from ..forms import AnswerForm

# 댓글 등록
@login_required(login_url="common:login")
def answer_create(request, board_id):
    # board_id 를 사용해 질문 가져오기
    board = Board.objects.get(id=board_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # 작성자 추가 (현재 로그인 사용자 : request.user)
            answer.nickname = request.user
            answer.create_date = timezone.now()
            answer.board = board
            answer.save()

            # detail에서 특정 영역 보여주기
            # http://1270.0.0.1:8000/board/305#answer_7
            return redirect(
                "{}#answer_{}".format(
                    # resolce_url() : 실제 호출되는 URL을 문자열로 반환
                    resolve_url("board:detail", question_id=board_id),
                    answer.id,
                )
            )
    else:
        form = AnswerForm()

    context = {"question": board, "form": form}

    return render(request, "board/question_detail.html", context)


# 답변 수정 - 원본 내용 찾은 후 수정
# 답변 수정 전에 로그인 확인 여부
@login_required(login_url="common:login")
def answer_modify(request, answer_id):
    # answer_id에 해당하는 데이터 가져오기
    answer = get_object_or_404(Answer, pk=answer_id)

    # 작성자와 같은지 확인
    if request.user != answer.author:
        messages.error(request, "수정할 권한이 없습니다.")
        return redirect("board:detail", question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)

        # 유효성 검사
        if form.is_valid():
            answer = form.save(commit=False)
            answer.nickname = request.user  # 작성자
            answer.modify_date = timezone.now()  # 수정 날짜
            answer.save()

            # detail에서 특정 영역 보여주기
            # http://1270.0.0.1:8000/board/305#answer_7
            return redirect(
                # 앞 {} : 글 번호
                # 뒤 {} : answer.id
                "{}#answer_{}".format(
                    # resolce_url() : 실제 호출되는 URL을 문자열로 반환
                    resolve_url("board:detail", board_id=answer.board_id),
                    answer.id,
                )
            )

    else:
        form = AnswerForm(instance=answer)
    return render(request, "board/answer_form.html", {"form": form})


# 댓글 삭제
@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    # 삭제할 데이터 찾기
    answer = get_object_or_404(Answer, pk=answer_id)

    # 작성자와 같은지 확인
    if request.user != answer.nickname:
        messages.error(request, "삭제할 권한이 없습니다.")
        return redirect("board:detail", board_id=answer.board.id)

    answer.delete()

    # 내용보기로 들어가기
    return redirect("board:detail", board_id=answer.board_id)
