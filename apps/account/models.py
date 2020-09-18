#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from apps.category.models import *
from django.core.validators import MaxValueValidator
from django.db.models import Avg
from hashids import Hashids

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

def structure_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "structure/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_structure" + "." + ext
    return os.path.join(path, format)

def machine_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "machine/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_machine" + "." + ext
    return os.path.join(path, format)

def certification_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "certification/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_certification" + "." + ext
    return os.path.join(path, format)

def process_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "process/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_process" + "." + ext
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
# Model   : User
# Description : 회원 모델
# ------------------------------------------------------------------
USER_TYPE = [
    (0, "CLIENT"),
    (1, "PARTNER")
]
class User(AbstractUser):

    # 공통 부분
    username = models.CharField('이메일', max_length=256, default=get_default_hash_id, unique=True)
    type = models.IntegerField('유저타입', default=0, choices=USER_TYPE)
    password = models.CharField(max_length=256)
    phone = models.CharField('휴대폰 번호', max_length=32, blank=True)
    marketing = models.BooleanField('마케팅동의여부', default=True, null=True)
    last_activity = models.DateTimeField('최근 활동', default = None, blank = True, null = True)

    class Meta:
        verbose_name = '가입자'
        verbose_name_plural = '가입자'
        
    @property
    def is_update(self):
        if self.username and self.type and self.password:
            return True
        else:
            return False

# ------------------------------------------------------------------
# Model   : Client
# Description : 클라이언트 모델
# ------------------------------------------------------------------

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='유저')
    name = models.CharField('업체명', max_length=256, null=True)
    title = models.CharField('직급', max_length=256, null=True)
    path = models.CharField('방문경로', max_length=256, null=True)
    business = models.CharField('업종', max_length=256, null=True)
    class Meta:
        verbose_name = '클라이언트'
        verbose_name_plural = '클라이언트'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Clientclass
# Description : 결제에 따른 클라이언트의 Class
# ------------------------------------------------------------------

class Clientclass(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='클라이언트')
    client_class = models.IntegerField('클라이언트 클래스', default=0, null=True)
    created_at = models.DateTimeField('등록일자', auto_now_add=True)
    end_time = models.DateTimeField('클래스 종료 일자', null=True)

    class Meta:
        verbose_name = '클라이언트 클래스'
        verbose_name_plural = '클라이언트 클래스'

    def __str__(self):
        return str(self.id)


# ------------------------------------------------------------------
# Model   : Partner
# Description : 파트너 모델
# ------------------------------------------------------------------
PARTNER_GRADE = [
    (0, "파트너 X"),
    (1, "일반 파트너"),
    (2, "프리미엄 파트너")
]
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='유저')
    name = models.CharField('업체명', max_length=256, null=True)
    logo = models.ImageField('로고', upload_to=partner_update_filename, blank=True, null=True)
    #지역
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="시/도", null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="구", null=True)
    career = models.CharField('설립일', max_length=256, null=True)
    employee = models.CharField('근로자수', max_length=256, null=True)
    revenue = models.CharField('매출(백만원)', max_length=256, null=True)
    info_company = models.TextField('회사소개', blank=True, null=True)
    info_biz = models.TextField('주요사업', blank=True, null=True)
    history = models.TextField('주요이력', blank=True, null=True)
    deal = models.TextField('주요거래처', blank=True, null=True)
    category_middle = models.ManyToManyField(Develop, verbose_name='의뢰가능분야', related_name='category_middle')
    #possible_set = models.ManyToManyField(Subclass, verbose_name='개발가능제품분야', related_name='possible_product')
    history_set = models.ManyToManyField(Subclass, verbose_name='진행한제품들', related_name='history_product')
    #결제
    coin = models.IntegerField('코인', default=2000, null=True)
    #회원가입 시 파일
    file = models.FileField('회사소개 및 포토폴리오파일', upload_to=partner_update_filename, blank=True, null=True)
    avg_score = models.DecimalField('평균점수', default=0, max_digits=5, decimal_places=2, null=True)
    # 파트너 여부
    #is_partner = models.BooleanField('파트너여부', default=True, null=True)
    # 파트너 등급
    grade = models.IntegerField('파트너 등급', default=0, choices=PARTNER_GRADE, null=True)
    # 안심번호가 아닌 실제 전화번호
    real_phone = models.CharField('실제 휴대폰 번호', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = '파트너'
        verbose_name_plural = '파트너'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Portfolio
# Description : 포트폴리오 모델
# ------------------------------------------------------------------
class Portfolio(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    img_portfolio = models.ImageField('포토폴리오 이미지', upload_to=portfolio_update_filename, null=True)
    is_main = models.BooleanField('메인 여부', default=False)

    class Meta:
        verbose_name = '     포트폴리오'
        verbose_name_plural = '     포트폴리오'

    def __str__(self):
        return str(self.partner.name) + " 포트폴리오"

# ------------------------------------------------------------------
# Model   : Structure
# Description : 조직도 모델
# ------------------------------------------------------------------
class Structure(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    img_structure = models.ImageField('조직도 이미지', upload_to=structure_update_filename, null=True)
    is_main = models.BooleanField('메인 여부', default=False)

    class Meta:
        verbose_name = '     조직도'
        verbose_name_plural = '     조직도'

    def __str__(self):
        return str(self.partner.name) + " 조직도"

# ------------------------------------------------------------------
# Model   : Machine
# Description : 보유장비 모델
# ------------------------------------------------------------------
class Machine(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    img_machine = models.ImageField('보유장비 이미지', upload_to=machine_update_filename, null=True)
    is_main = models.BooleanField('메인 여부', default=False)

    class Meta:
        verbose_name = '     보유장비'
        verbose_name_plural = '     보유장비'

    def __str__(self):
        return str(self.partner.name) + " 보유장비"

# ------------------------------------------------------------------
# Model   : Certification
# Description : 포트폴리오 모델
# ------------------------------------------------------------------
class Certification(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    img_certification = models.ImageField('보유인증서 이미지', upload_to=certification_update_filename, null=True)
    is_main = models.BooleanField('메인 여부', default=False)

    class Meta:
        verbose_name = '     보유인증서'
        verbose_name_plural = '     보유인증서'

    def __str__(self):
        return str(self.partner.name) + " 보유인증서"

# ------------------------------------------------------------------
# Model   : Process
# Description : 진행공정 모델
# ------------------------------------------------------------------
class Process(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    img_process = models.ImageField('진행공정 이미지', upload_to=process_update_filename, null=True)
    is_main = models.BooleanField('메인 여부', default=False)

    class Meta:
        verbose_name = '     진행공정'
        verbose_name_plural = '     진행공정'

    def __str__(self):
        return str(self.partner.name) + " 진행공정"
        
# ------------------------------------------------------------------
# Model   : LoginLog
# Description : 로그인 로그 저장 모델
# ------------------------------------------------------------------

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'User', null=True)
    created_at = models.DateTimeField('로그인일자', auto_now_add=True)
    type = models.IntegerField('유저타입', default=0, choices=USER_TYPE)


    class Meta:
        verbose_name = '로그인 로그'
        verbose_name_plural = '로그인 로그'
        ordering = ('-created_at',)

    def __str__(self):
        return '{}_log'.format(self.user)

class Path(models.Model):
    path = models.CharField('방문경로', max_length=256, null=True)


    class Meta:
        verbose_name = '방문경로'
        verbose_name_plural = '방문경로'

    def __str__(self):
        return str(self.path)

class Business(models.Model):
    business = models.CharField('업종', max_length=256, null=True)


    class Meta:
        verbose_name = '업종'
        verbose_name_plural = '업종'

    def __str__(self):
        return str(self.business)
