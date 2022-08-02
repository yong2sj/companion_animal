from . import views
from django.urls import path

# 네임스페이스 지정
app_name = "board"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>", views.detail, name="detail"),
    path("board/create", views.board_create, name="board_create"),
    # /board/question/modify/ question_modify 
    path("board/modify/<int:question_id>", views.board_modify, name="board_modify"),
    # /board/question/delete/ question_delete 
    path("board/delete/<int:question_id>", views.board_delete, name="board_delete"),
]