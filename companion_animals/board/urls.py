from . import views
from django.urls import path

# 네임스페이스 지정
app_name = "board"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>", views.detail, name="detail"),
    path("question/create", views.question_create, name="question_create"),
    # /board/question/modify/ question_modify
    path(
        "question/modify/<int:question_id>",
        views.question_modify,
        name="question_modify",
    ),
    # /board/question/delete/ question_delete
    path(
        "question/delete/<int:question_id>",
        views.question_delete,
        name="question_delete",
    ),
]
