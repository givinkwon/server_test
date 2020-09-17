#-*- coding: cp949 -*-
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

#�ð� ���� �Լ�
from django.utils import timezone
from datetime import date


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

def answer_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "answer/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_answer" + "." + ext
    return os.path.join(path, format)

def time():
    time = timezone.now()
    return time

# ------------------------------------------------------------------
# Model   : Project
# Description : ������Ʈ ��
# ------------------------------------------------------------------
class Project(models.Model):

    class Meta:
        verbose_name = '     ������Ʈ'
        verbose_name_plural = '     ������Ʈ'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Request
# Description : �Ƿڼ� ��
# ------------------------------------------------------------------
class Request(models.Model):
       
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='�ۼ�Ŭ���̾�Ʈ')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='������Ʈ')
    product = models.ForeignKey(Subclass, on_delete=models.CASCADE, verbose_name='�Ƿ���ǰ')
    # ��������
    category = models.ManyToManyField(Develop, verbose_name='�Ƿںо�')
    #��������
    name = models.CharField('�Ƿ���ǰ��', max_length=256, blank=True, null=True)
    price = models.CharField('������', max_length=256, blank=True, null=True)
    day = models.CharField('���������Ʈ�Ⱓ(��)', max_length=256, blank=True, null=True)
    content = RichTextUploadingField('�Ƿڳ���', blank=True, null=True)
    file = models.FileField('�Ƿ�����', upload_to=request_update_filename, blank=True, null=True)
    #������� ��Ͽ�
    created_at = models.DateTimeField('�������', default=time)
    #�Ƿڼ� �ϼ��Ǿ��� ��
    #add_meeting = models.BooleanField('�߰��� �����ϱ� ����', default=False, null=True)
    #�Ƿڼ� ���� �Ǿ��� ��
    send_information = models.BooleanField('�Ƿڼ� ���� īī���� �߼� ����', default=False, null=True)
    active_save = models.BooleanField('Ȱ�� ��ȭ ����', default=True, null=True)

    @property
    def apply_count(self):
        return Answer.objects.filter(project=self.project).count()

    @property
    def time_out(self):
        now = timezone.now()
        return (now - self.created_at)

    @property
    def active(self):
        print(self.time_out.days)
        active=self.time_out.days
        if active >= 1:
            if self.active_save is True:
                self.active_save = False
                self.save()
            return False
        return True

    @property
    def coin(self):
        category_qs = self.category.all()
        #������ ��� �������� ����Ʈȭ�ϱ�
        category_coin =category_qs.values_list('coin', flat=True)
        #����Ʈȭ �� �� ��� ���ϱ�
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
        verbose_name = '     ��û�� �Ƿ�'
        verbose_name_plural = '     ��û�� �Ƿ�'

    def __str__(self):
        return str(self.name)

# ------------------------------------------------------------------
# Model   : Select_save
# Description : �Ƿμ��� ����Ǵ� ��������/�亯 ��
# ------------------------------------------------------------------
class Select_save(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='�Ƿڼ�')
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='���ߺо�')
    question = models.CharField('��������', max_length=256, blank=True, null=True)
    answer = models.CharField('���������亯', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     �Ƿڼ��� ����Ǵ� ��������/�亯'
        verbose_name_plural = '     �Ƿڼ��� ����Ǵ� ��������/�亯'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Select
# Description : �������� ��
# ------------------------------------------------------------------
class Select(models.Model):
    # ��������
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='���ߺо��ߺз�')
    request = models.TextField('��������', blank=True, null=True)


    class Meta:
        verbose_name = '     ��������'
        verbose_name_plural = '     ��������'

    def __str__(self):
        return str(self.request)

# ------------------------------------------------------------------
# Model   : Content
# Description : ������������ ��.
# ------------------------------------------------------------------
class Content(models.Model):
    # ��������
    request = models.ForeignKey(Select, on_delete=models.CASCADE, verbose_name='��������')
    content1 = models.CharField('������1', max_length=256, blank=True, null=True)
    content2 = models.CharField('������2', max_length=256, blank=True, null=True)
    content3 = models.CharField('������3', max_length=256, blank=True, null=True)
    content4 = models.CharField('������4', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     ��������������'
        verbose_name_plural = '     ��������������'

    def __str__(self):
        return str(self.request)

# ------------------------------------------------------------------
# Model   : Common
# Description : �������� ��
# ------------------------------------------------------------------
class Common(models.Model):
    # ��������
    product = models.CharField('�Ƿ���ǰ��', max_length=256, blank=True, null=True)
    price = models.CharField('������', max_length=256, blank=True, null=True)
    day = models.CharField('���������Ʈ�Ⱓ(��)', max_length=256, blank=True, null=True)
    content = RichTextUploadingField('�Ƿڳ���')
    file = models.FileField('�Ƿ�����', upload_to=request_update_filename, blank=True, null=True)


    class Meta:
        verbose_name = '     ��������'
        verbose_name_plural = '     ��������'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Answer
# Description : ���ȼ� ��
# ------------------------------------------------------------------

INFO = [
(0, "���� ��Ȯ��"),
(1, "��Ʈ�ʻ� ���� Ȯ��"),
(2, "��Ʈ�ʻ� ����"),
]

MEETING_STATE = [
    (0, "NOTSUBMIT"), # ���õ��� ����
    (1, "YES"),
    (2, "NO"),
]
class Answer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Ŭ���̾�Ʈ")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="������Ʈ", null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="�ۼ� ��Ʈ��")
    category = models.TextField('���� �о�', blank=True, null=True)
    people = models.TextField('���� ���� �ο�', blank=True, null=True)
    price = models.TextField('���� �Է�', blank=True, null=True)
    strategy = models.TextField('���� ���� ���', blank=True, null=True)
    period = models.TextField('���� ���� �Ⱓ', blank=True, null=True)

    day = models.IntegerField('�� ���� �Ⱓ', default=0)
    all_price = models.IntegerField('���� ����', default=0)

    expert = models.TextField('������ �� ����', blank=True, null=True)
    file = models.FileField('�Ƿ�����', upload_to=answer_update_filename, blank=True, null=True)

    created_at = models.DateTimeField('�������', auto_now_add=True)
    state = models.IntegerField('���� ����', default=0, choices=MEETING_STATE)
    active = models.BooleanField('Ȱ��ȭ����', default=False)

    open_time = models.DateTimeField('���ȼ� ���� �ð�', default = None, blank=True, null = True)
    send_meeting = models.BooleanField('���� �ȳ� ī�� ���� ����', default=False)
    info_check = models.IntegerField('����Ȯ�ο���', default=0, null=True, blank=True, choices=INFO)

    @property # ���� ���� �ð� üũ
    def time_out(self):
        now = timezone.now()
        if self.open_time is not None:
          return (now - self.open_time)

        return  False

    @property # ���� ���� �Ϸ� ������ ī�� ������
    def send_kakao(self):
        if self.open_time is not None:

            active = self.time_out.days
            if active >= 1:
                if self.send_meeting is False:
                    self.send_meeting = True
                    self.save()
                return False
            return False

        return False

    @property
    def see_phone(self): # ��ȭ��ȣ ��ư�� ������ ������
        if self.active:
            return True
        else:
            return False

    @property
    def see_review(self): # ���� ��ư�� ������ ������
        if self.state == 1:
            return True
        else:
            return False

    @property
    def down_chage(self): # �Ʒ��� ���ȼ��� Ȱ��ȭ��ų ������
        if self.active and self.state:
             return True
        else:
             return False

    class Meta:
        verbose_name = '     ���ȼ�'
        verbose_name_plural = '     ���ȼ�'

    def __str__(self):
        self.send_kakao
        return str(self.id)


# ------------------------------------------------------------------
# Model   : Review
# Description : ���� ��
# ------------------------------------------------------------------
class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name ="�ۼ�Ŭ���̾�Ʈ")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="������Ʈ")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��")
    price_score = models.PositiveSmallIntegerField('���� ������', default=0, validators=[MaxValueValidator(5), ])
    time_score = models.PositiveSmallIntegerField('�����ӵ� �� ����', default=0, validators=[MaxValueValidator(5), ])
    talk_score = models.PositiveSmallIntegerField('�ǻ����', default=0, validators=[MaxValueValidator(5), ])
    expert_score = models.PositiveSmallIntegerField('������', default=0, validators=[MaxValueValidator(5), ])
    result_score = models.PositiveSmallIntegerField('����� �� ǰ��', default=0, validators=[MaxValueValidator(5), ])
    content_good = models.TextField('���� �ı�', blank=True, null=True)
    content_bad = models.TextField('��� �ı�', blank=True, null=True)

    @property
    def avg_score(self):
        avg_score = (self.price_score + self.time_score + self.talk_score + self.expert_score + self.result_score)/5
        return avg_score

    class Meta:
        verbose_name = '���亰��'
        verbose_name_plural = '���亰��'

    def __str__(self):
        return str(self.id)
