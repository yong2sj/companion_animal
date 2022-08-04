# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, RoomCount
from tools.utils import get_client_ip


def index(request):
    rooms = Room.objects.filter(count_users__lte=0)
    for room in rooms:
        room.delete()
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, "chat/index.html", context)


@login_required
def enter_room(request, room_pk):
    if request.user.is_authenticated:
        user = request.user
        room = Room.objects.get(pk=room_pk)

        ### 인원 추가
        # 사용자 ip 가져오기
        ip = get_client_ip(request)

        # 찾은 ip가 BoardCount 테이블에 있는지 확인
        cnt = RoomCount.objects.filter(ip=ip, room=room).count()

        if cnt == 0:  # 조회수 증가
            # 모델 생성
            rc = RoomCount(ip=ip, room=room)
            # 저장
            rc.save()
            # question 테이블의 view_cnt 1 증가
            if room.count_users:
                room.count_users += 1
            else:
                room.count_users = 1
            room.save()

        room.save()
        context = {
            "room": room,
            "user": user,
        }
        return render(request, "chat/room.html", context)


@login_required
def create(request):
    if request.user.is_authenticated:
        room_name = request.POST["roomname"]
        room = Room.objects.create(room_name=room_name)
        return redirect("chat:room", room.pk)
