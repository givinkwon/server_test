import os, datetime, uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from apps.category.models import *
from apps.account.models import *
from typing import TYPE_CHECKING

from ckeditor_uploader.fields import RichTextUploadingField

from hashids import Hashids
from django.core.validators import MaxValueValidator

#시간 관련 함수
from django.utils import timezone
from datetime import date

now = timezone.localtime()

# Create your models here.
def get_default_hash_id():
    hashids = Hashids(salt=settings.SECRET_KEY, min_length=6)
    try:
        user_id = User.objects.latest('id').id + 1
    except:
        user_id = 1
    return hashids.encode(user_id)


def business_license_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "business_license/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_" + instance.username + "_business" + "." + ext
    return os.path.join(path, format)


def partner_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "partner/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_partner" + "." + ext
    return os.path.join(path, format)


def portfolio_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "portfolio/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_portfolio" + "." + ext
    return os.path.join(path, format)


def user_portfolio_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "user_portfolio/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_portfolio" + "." + ext
    return os.path.join(path, format)


def request_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "request/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_request" + "." + ext
    return os.path.join(path, format)


def maincategory_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "maincategory/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_maincategory" + "." + ext
    return os.path.join(path, format)


def category_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "category/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_category" + "." + ext
    return os.path.join(path, format)


def subclass_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "subclass/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_subclass" + "." + ext
    return os.path.join(path, format)


# ------------------------------------------------------------------
# Model   : Project
# Description : 프로젝트 모델
# ------------------------------------------------------------------
class Project(models.Model):

    class Meta:
        verbose_name = '     프로젝트'
        verbose_name_plural = '     프로젝트'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Request
# Description : 의뢰서 모델
# ------------------------------------------------------------------
class Request(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='작성클라이언트')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='프로젝트')
    product = models.ForeignKey(Subclass, on_delete=models.CASCADE, verbose_name='의뢰제품')
    # 선택질문
    category = models.ManyToManyField(Develop, verbose_name='의뢰분야')
    #공통질문
    name = models.CharField('의뢰제품명', max_length=256, blank=True, null=True)
    price = models.IntegerField('희망비용', default=0)
    day = models.IntegerField('희망프로젝트기간(일)', default=0)
    content = RichTextUploadingField('의뢰내용')
    file = models.FileField('의뢰파일', upload_to=request_update_filename, blank=True, null=True)
    #등록일자 기록용
    created_at = models.DateTimeField('등록일자', auto_now_add=True)
    #의뢰서 완성되었는 지
   # complete = models.BooleanField('활성화여부', default=False, null=True)
    @property
    def apply_count(self):
        return Answer.objects.filter(project=self.project).count()

    @property
    def time_out(self):
        return (now - self.created_at)

    @property
    def active(self):
        active=self.time_out.days
        if active >= 1:
            return False
        return True

    @property
    def coin(self):
        category_qs = self.category.all()
        #쿼리셋 밸류 가져오고 리스트화하기
        category_coin =category_qs.values_list('coin', flat=True)
        #리스트화 및 값 모두 더하기
        category_coin = list(category_coin)
        category_coin_sum = sum(category_coin)
        price = category_coin_sum
        return price

    @property
    def complete(self):
        if self.name and self.price and self.day and self.content:
            return True
        return False

    class Meta:
        verbose_name = '     요청된 의뢰'
        verbose_name_plural = '     요청된 의뢰'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Select_save
# Description : 의로서에 저장되는 선택질문/답변 모델
# ------------------------------------------------------------------
class select_save(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='의뢰서')
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='의뢰서')
    question = models.CharField('선택질문', max_length=256, blank=True, null=True)
    answer = models.CharField('선택질문답변', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     의뢰서에 저장되는 선택질문/답변'
        verbose_name_plural = '     의뢰서에 저장되는 선택질문/답변'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Select
# Description : 선택질문 모델
# ------------------------------------------------------------------
class Select(models.Model):
    # 선택질문
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='개발분야중분류')
    request = models.TextField('선택질문', blank=True, null=True)


    class Meta:
        verbose_name = '     선택질문'
        verbose_name_plural = '     선택질문'

    def __str__(self):
        return str(self.request)

# ------------------------------------------------------------------
# Model   : Content
# Description : 선택질문내용 모델
# ------------------------------------------------------------------
class Content(models.Model):
    # 선택질문
    request = models.ForeignKey(Select, on_delete=models.CASCADE, verbose_name='선택질문')
    content1 = models.CharField('컨텐츠1', max_length=256, blank=True, null=True)
    content2 = models.CharField('컨텐츠2', max_length=256, blank=True, null=True)
    content3 = models.CharField('컨텐츠3', max_length=256, blank=True, null=True)
    content4 = models.CharField('컨텐츠4', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     선택질문컨텐츠'
        verbose_name_plural = '     선택질문컨텐츠'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Common
# Description : 공통질문 모델
# ------------------------------------------------------------------
class Common(models.Model):
    # 공통질문
    product = models.CharField('의뢰제품명', max_length=256, blank=True, null=True)
    price = models.IntegerField('희망비용', default=0)
    day = models.IntegerField('희망프로젝트기간(일)', default=0)
    content = RichTextUploadingField('의뢰내용')
    file = models.FileField('의뢰파일', upload_to=request_update_filename, blank=True, null=True)


    class Meta:
        verbose_name = '     공통질문'
        verbose_name_plural = '     공통질문'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Answer
# Description : 제안서 모델
# ------------------------------------------------------------------

MEETING_STATE = [
    (0, "NOTSUBMIT"), # 선택되지 않음
    (1, "YES"),
    (2, "NO"),
]
class Answer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="클라이언트")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="프로젝트", null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="작성 파트너")
    price = models.IntegerField('제안비용', default=0)
    day = models.CharField('제안개발기간', max_length=256, blank=True, null=True)
    expert = models.CharField('전문성 및 경험', max_length=256, blank=True, null=True)
    strategy = models.CharField('제안 전략', max_length=256, blank=True, null=True)
    created_at = models.DateTimeField('등록일자', auto_now_add=True)
    state = models.IntegerField('미팅 상태', default=0, choices=MEETING_STATE)
    active = models.BooleanField('활성화여부', default=False)

    @property
    def see_phone(self): # 전화번호 버튼을 보여줄 것인지
        if self.active:
            return True
        else:
            return False

    @property
    def see_review(self): # 리뷰 버튼을 보여줄 것인지
        if self.state == 1:
            return True
        else:
            return False

    @property
    def down_chage(self): # 아래의 제안서를 활성화시킬 것인지
        if self.active and self.state:
             return True
        else:
             return False

    class Meta:
        verbose_name = '     제안서'
        verbose_name_plural = '     제안서'

    def __str__(self):
        return str(self.id)


# ------------------------------------------------------------------
# Model   : Review
# Description : 리뷰 모델
# ------------------------------------------------------------------
class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name ="작성클라이언트")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="프로젝트")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너")
    price_score = models.PositiveSmallIntegerField('가격 만족도', default=0, validators=[MaxValueValidator(5), ])
    time_score = models.PositiveSmallIntegerField('일정 준수', default=0, validators=[MaxValueValidator(5), ])
    talk_score = models.PositiveSmallIntegerField('의사소통', default=0, validators=[MaxValueValidator(5), ])
    expert_score = models.PositiveSmallIntegerField('전문성', default=0, validators=[MaxValueValidator(5), ])
    result_score = models.PositiveSmallIntegerField('결과 만족도', default=0, validators=[MaxValueValidator(5), ])
    content = models.CharField('리뷰내용', max_length=256, blank=True, null=True)

    @property
    def avg_score(self):
        avg_score = (self.price_score + self.time_score + self.talk_score + self.expert_score + self.result_score)/5
        return avg_score

    class Meta:
        verbose_name = '리뷰별점'
        verbose_name_plural = '리뷰별점'

    def __str__(self):
        return str(self.id)
