from unicodedata import category
from django.db import models
from common.models import Profile
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
    nickname = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="nickname_board"
    )
    # 카테고리
    category = models.CharField(max_length=20)
    # 생성 날짜
    create_date = models.DateTimeField()
    # 수정된 날짜 보여주기
    # black=True : form.is_valid()를 통한 폼 검사시 값이 없어도 됨
    update_date = models.DateTimeField(null=True, blank=True)
    # 추천수
    # ManyToManyField : 다대다
    voter = models.ManyToManyField(User, related_name="vote_board")
    # 조회수
    view_cnt = models.BigIntegerField(default=0)


# 댓글
class Answer(models.Model):
    # Answer 테이블과 Board 테이블의 외래키 제약 조건
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # 댓글 내용
    content = models.TextField()
    # 작성자
    nickname = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="nickname_answer"
    )
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
    nickname = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="nickname_comment"
    )
    # 생성 날짜
    create_date = models.DateTimeField()
    # 수정된 날짜 보여주기
    # black=True : form.is_valid()를 통한 폼 검사시 값이 없어도 됨
    update_date = models.DateTimeField(null=True, blank=True)


class BoardCount(models.Model):
    ip = models.CharField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.ip
