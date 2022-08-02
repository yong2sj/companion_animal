from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Answer, Comment
from ..forms import CommentForm

# 대댓글 등록
@login_required(login_url="common:login")
def comment_create(request, answer_id):

    # 질문 가져오기 - models.py에서 질문 정로를 question에서 담아서 옴
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            # 추가 작업 (forms.py에서 안한 작업)
            comment.nickname = request.user  # 로그인 사용자
            comment.create_date = timezone.now()  # 현재 시간 날짜
            comment.answer = answer
            comment.save()

            # 앵커가 들어온 후
            return redirect(
                "{}#comment_{}".format(
                    resolve_url("board:detail", comment.answer.board.id), comment.id
                )
            )

    else:
        form = CommentForm()

    return render(request, "board/comment_form.html", {"form": form})


# 대댓글 수정
@login_required(login_url="common:login")
def comment_modify(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)

    # 작성자와 같은지 확인
    if request.user != comment.author:
        messages.error(request, "댓글을 수정할 권한이 없습니다.")
        return redirect("board:detail", board_id=comment.answer.board.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()

            # 앵커가 들어온 후
            return redirect(
                "{}#comment_{}".format(
                    resolve_url("board:detail", board_id=comment.answer.board.id),
                    comment.id,
                )
            )
    else:
        form = CommentForm(instance=comment)

    return render(request, "board/comment_form.html", {"form": form})


# 대댓글 삭제
@login_required(login_url="common:login")
def comment_delete(request, comment_id):
    # 삭제할 데이터 찾기
    comment = get_object_or_404(Comment, pk=comment_id)

    # 작성자와 같은지 확인
    if request.user != comment.nickname:
        messages.error(request, "댓글을 삭제할 권한이 없습니다.")
        return redirect("board:detail", question_id=comment.answer.board.id)

    # 댓글 삭제 명령어
    comment.delete()

    # 내용보기로 들어가기
    return redirect("board:detail", question_id=comment.answer.board.id)
