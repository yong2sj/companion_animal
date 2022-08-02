from django.db import models
from django.contrib.auth.models import User

# 게시글
class Board(models.Model):
    # 구별
    gu = models.CharField(max_length=5)
    # 제목
    subject = models.CharField(max_length=200)
    # 내용
    content = models.TextField()
    # 작성자
    nickname = models.ForeignKey(User, on_delete=models.CASCADE)
    # 생성 날짜
    create_date = models.DateTimeField()
    # 수정된 날짜 보여주기
    # black=True : form.is_valid()를 통한 폼 검사시 값이 없어도 됨
    update_date = models.DateTimeField(null=True, blank=True)

    # 추천수
    # ManyToManyField : 다대다
    voter = models.ManyToManyField(User, related_name="vote_board")


# 댓글
class Answer(models.Model):
    # Answer 테이블과 Board 테이블의 외래키 제약 조건
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # 댓글 내용
    content = models.TextField()
    # 작성자
    nickname = models.ForeignKey(User, on_delete=models.CASCADE)
    # 생성 날짜
    create_date = models.DateTimeField()
    # 수정된 날짜 보여주기
    # black=True : form.is_valid()를 통한 폼 검사시 값이 없어도 됨
    update_date = models.DateTimeField(null=True, blank=True)


# 대댓글
class Comment(models.Model):
    # Answer 테이블과 Board 테이블의 외래키 제약 조건
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # 댓글 내용
    content = models.TextField()
    # 작성자
    nickname = models.ForeignKey(User, on_delete=models.CASCADE)
    # 생성 날짜
    create_date = models.DateTimeField()
    # 수정된 날짜 보여주기
    # black=True : form.is_valid()를 통한 폼 검사시 값이 없어도 됨
    update_date = models.DateTimeField(null=True, blank=True)


# 프로필
class Profile(models.Model):
    # 연락처
    phone = models.CharField(max_length=15)
    # 반려동물 종
    species = models.CharField(max_length=10)
    # 반려동물 이름
    pet_name = models.CharField(max_length=10)
    # 사진 추가
    # image = models.ImageField(upload_to="profile/", default="default.png")
