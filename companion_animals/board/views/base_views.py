from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from ..models import Board


def main(request):
    return render(request, "board/board_main.html")
    
# 게시판 목록 조회
def index(request):
    # question 테이블 내용 조회
    # Question.objects.all()

    page = request.GET.get("page", 1)  # http://127.0.0.1:8000/board/?page=1
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "")
    sort_a = request.GET.get("sort_a", "recents")

    # annotate() : voter라는 필드의 개수를 센 후 nun_voter라는 임시 필드를 추가해 주는 함수
    if sort_a == "recents":
        board_list = Board.objects.order_by("-create_date")
    elif sort_a == "recommends":
        board_list = Board.objects.annotate(num_voter=Count("voter")).order_by(
            "-num_voter", "-create_date"
        )
    else:
        board_list = Board.objects.annotate(num_answer=Count("answer")).order_by(
            "-num_answer", "-create_date"
        )
    
    # 행정 구 에 맞게 소팅
    if sort == "서울전체":
        pass
    else:
        board_list = board_list.filter(Q(gu__contains=sort))

    # 조회된 목록을 기준으로 검색 조건을 줘서 필터링
    # Q() : OR 조건으로 데이터를 조회
    # subject__contains(대소문자 구별)
    # subject__icontains(대소문자 구별 하지 않음)

    if keyword:
        board_list = board_list.filter(
            Q(subject__icontains=keyword)
            | Q(content__icontains=keyword)
            | Q(author__username__icontains=keyword)
            | Q(answer__author__username__icontains=keyword)
        ).distinct()

    paginator = Paginator(
        board_list, 10
    )  # Paginator 객체 생성(전체목록, 10) : 전체목록에서 10개씩 가져오기
    page_obj = paginator.get_page(page)

    context = {"board_list": page_obj, "page": page, "keyword": keyword, "sort": sort, "sort_a":sort_a}

    return render(request, "board/board_list.html", context)


# 게시판 상세페이지
def detail(request, board_id):

    ### 페이지 나누기 추가
    page = request.GET.get("page", 1)  # http://127.0.0.1:8000/board/?page=1
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "")

    # 없는 id를 요청했을 때 웹 페이지에 오류 메세지가 그대로 출력
    board = get_object_or_404(Board, id=board_id)

    ### 조회수 추가
    # 사용자 ip 가져오기
    # ip = get_client_ip(request)

    # 찾은 ip가 QuestionCount 테이블에 있는지 확인
    # cnt = QuestionCount.objects.filter(ip=ip, question=question).count()

    # if cnt == 0: # 조회수 증가
    #     # 모델 생성
    #     qc = QuestionCount(ip=ip, question=question)
    #     # 저장
    #     qc.save()
    #     # question 테이블의 view_cnt 1 증가
    #     if question.view_cnt:
    #         question.view_cnt += 1
    #     else:
    #         question.view_cnt = 1
    #     question.save()
    context = {"board": board, "page": page, "keyword": keyword, "sort": sort}
    return render(request, "board/board_detail.html", context)
