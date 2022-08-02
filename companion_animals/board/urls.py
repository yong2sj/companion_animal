from .views import base_views, answer_views, comment_views, board_views, vote_views
from django.urls import path

# 네임스페이스 지정
app_name = "board"

urlpatterns = [
    # 게시물 목록 보여주기
    path("", base_views.index, name="index"),
    # 게시물 상세페이지 보여주기
    path("<int:board_id>", base_views.detail, name="detail"),
    # 게시물 등록
    path("board/create", board_views.board_create, name="board_create"),
    # 게시물 수정
    # /board/board/modify/ board_modify
    path(
        "board/modify/<int:board_id>",
        board_views.board_modify,
        name="board_modify",
    ),
    # 게시물 삭제
    # /board/board/delete/board_delete
    path(
        "board/delete/<int:board_id>",
        board_views.board_delete,
        name="board_delete",
    ),
    # 댓글 등록
    # /board/answer/create/1
    path(
        "answer/create<int:board_id>",
        answer_views.answer_create,
        name="answer_create",
    ),
    # 댓글 수정
    # /board/answer/modify/1 answer.id : 값을 받을 변수 answer_id
    path(
        "answer/modify/<int:answer_id>",
        answer_views.answer_modify,
        name="answer_modify",
    ),
    # 댓글 삭제
    # /board/answer/delete/1 answer.id : 값을 받을 변수 answer_id
    path(
        "answer/delete/<int:answer_id>",
        answer_views.answer_delete,
        name="answer_delete",
    ),
    # 대댓글 작성
    # /board/comment/create/answer_id
    path(
        "comment/create/<int:answer_id>",
        comment_views.comment_create,
        name="comment_create",
    ),
    # 대댓글 수정
    path(
        "comment/modify/<int:comment_id>",
        comment_views.comment_modify,
        name="comment_modify",
    ),
    # 대댓글 삭제
    path(
        "comment/delete/<int:comment_id>",
        comment_views.comment_delete,
        name="comment_delete",
    ),
    # 질문 추천 수
    path(
        "vote/board/<int:board_id>",
        vote_views.vote_board,
        name="vote_board",
    ),
]
