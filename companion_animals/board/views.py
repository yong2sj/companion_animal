from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Board, BoardCount

# from django.core.paginator import Paginator
# from django.db.models import Q, Count
# from tools.utils import get_client_ip

# index페이지
def index(request):
    # 게시판 목록 전체 보여주기
    Board.objects.all()
    # 주소줄에 따라옴
    # 페이지 나누기
    # http://127.0.0.1:8000/board/?page=1
    # page = request.GET.get("page", 1)
    # keyword
    # keyword = request.GET.get("keyword", "")
    # sort
    # sort = request.GET.get("sort", "")
    return render(request, "board/index.html")


# 상세페이지
def detail(request, board_id):
    # get : 없는 id를 요청했을 때 웹 페이지에 오류 메세지가 그대로 출력
    # question = Question.objects.get(id=question_id)

    # get_object_or_404 : 오류가 나면 Page not found 로 보여줌
    board = get_object_or_404(Board, id=board_id)

    return render(request, "board/detail.html")
