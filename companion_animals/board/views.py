from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Board, Profile
from .forms import BoardForm

def index(request):
    """
    질문목록
    """
    # return HttpResponse("Board")

    # question 테이블 내용 조회
    # Question.objects.all()

    page = request.GET.get("page", 1)  # http://127.0.0.1:8000/board/?page=1
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "")

    # 날짜 최신순으로 목록 조회
    # question_list = Question.objects.order_by("-create_date")

    # annotate() : voter라는 필드의 개수를 센 후 nun_voter라는 임시 필드를 추가해 주는 함수
    if sort == "recent":
        board_list = Board.objects.order_by("-create_date")
    elif sort == "recommend":
        board_list = Board.objects.annotate(num_voter=Count('voter')) \
                                        .order_by('-num_voter', '-create_date')
    else:
        board_list = Board.objects.annotate(num_answer=Count('answer')) \
                                        .order_by('-num_answer', '-create_date')

    # 조회된 목록을 기준으로 검색 조건을 줘서 필터링
    # Q() : OR 조건으로 데이터를 조회
    # subject__contains(대소문자 구별)
    # subject__icontains(대소문자 구별 하지 않음)

    if keyword:
        board_list = board_list.filter(
            Q(subject__icontains=keyword)
            |Q(content__icontains=keyword)
            |Q(author__username__icontains=keyword)
            |Q(answer__author__username__icontains=keyword)
        ).distinct()

    paginator = Paginator(board_list, 10) # Paginator 객체 생성(전체목록, 10) : 전체목록에서 10개씩 가져오기
    page_obj = paginator.get_page(page)

    context = {"board_list": page_obj, "page":page, "keyword":keyword, "sort":sort}
    
    return render(request, "board/board_list.html", context)


def detail(request, board_id):
    """
    질문 상세 조회
    """

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
    context = {"board":board, "page":page, "keyword":keyword, "sort":sort}
    return render(request, "board/board_detail.html", context)

 
@login_required(login_url='common:login')
def board_create(request):
    """
    질문등록
    """
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            # 작성자 추가(현재 로그인 사용자 : "request.user")
            profile = Profile.objects.get(user_id=request.user)
            board.nickname = profile.nickname
            board.save()
            return redirect("board:index")
    else:
        form = BoardForm()

    return render(request, "board/board_form.html", {"form": form})


@login_required(login_url='common:login')
def board_modify(request, board_id):
    """
    질문 수정(원본 내용 보여준 후 수정)
    """
    # question_id 값에 맞는 질문 찾아오기
    board = get_object_or_404(Board, pk=board_id)

    if request.user != board.author:
        messages.error(request, "수정할 권한이 없습니다.")
        return redirect('board:detail', board_id=board_id)

    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.modify_date = timezone.now()
            board.save()
            
            return redirect('board:detail', board_id=board_id)
    else:
        form = BoardForm(instance=board)

    return render(request, "board/board_form.html", {"form":form})

@login_required(login_url='common:login')
def board_delete(request, board_id):
    """
    질문 삭제
    """
    # question_id 질문 찾아오기
    board = get_object_or_404(Board, pk=board_id)

    if request.user != board.author:
        messages.error(request, "삭제할 권한이 없습니다.")
        return redirect('board:detail', board_id=board_id)

    # 삭제
    board.delete()

    return redirect('board:index')

def main(request):
    return render(request, "board/board_main.html")