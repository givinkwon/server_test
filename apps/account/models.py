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
# Description : ȸ�� ��
# ------------------------------------------------------------------
USER_TYPE = [
    (0, "CLIENT"),
    (1, "PARTNER")
]
class User(AbstractUser):

    # ���� �κ�
    username = models.CharField('�̸���', max_length=256, default=get_default_hash_id, unique=True)
    type = models.IntegerField('����Ÿ��', default=0, choices=USER_TYPE)
    password = models.CharField(max_length=256)
    phone = models.CharField('�޴��� ��ȣ', max_length=32, blank=True)
    marketing = models.BooleanField('�����õ��ǿ���', default=True, null=True)
    last_activity = models.DateTimeField('�ֱ� Ȱ��', default = None, blank = True, null = True)

    class Meta:
        verbose_name = '������'
        verbose_name_plural = '������'
        
    @property
    def is_update(self):
        if self.username and self.type and self.password:
            return True
        else:
            return False

# ------------------------------------------------------------------
# Model   : Client
# Description : Ŭ���̾�Ʈ ��
# ------------------------------------------------------------------

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='����')
    name = models.CharField('��ü��', max_length=256, null=True)
    title = models.CharField('����', max_length=256, null=True)
    path = models.CharField('�湮���', max_length=256, null=True)
    business = models.CharField('����', max_length=256, null=True)
    class Meta:
        verbose_name = 'Ŭ���̾�Ʈ'
        verbose_name_plural = 'Ŭ���̾�Ʈ'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Clientclass
# Description : ������ ���� Ŭ���̾�Ʈ�� Class
# ------------------------------------------------------------------

class Clientclass(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='Ŭ���̾�Ʈ')
    client_class = models.IntegerField('Ŭ���̾�Ʈ Ŭ����', default=0, null=True)
    created_at = models.DateTimeField('�������', auto_now_add=True)
    end_time = models.DateTimeField('Ŭ���� ���� ����', null=True)

    class Meta:
        verbose_name = 'Ŭ���̾�Ʈ Ŭ����'
        verbose_name_plural = 'Ŭ���̾�Ʈ Ŭ����'

    def __str__(self):
        return str(self.id)


# ------------------------------------------------------------------
# Model   : Partner
# Description : ��Ʈ�� ��
# ------------------------------------------------------------------
PARTNER_GRADE = [
    (0, "��Ʈ�� X"),
    (1, "�Ϲ� ��Ʈ��"),
    (2, "�����̾� ��Ʈ��")
]
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='����')
    name = models.CharField('��ü��', max_length=256, null=True)
    logo = models.ImageField('�ΰ�', upload_to=partner_update_filename, blank=True, null=True)
    #����
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="��/��", null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="��", null=True)
    career = models.CharField('������', max_length=256, null=True)
    employee = models.CharField('�ٷ��ڼ�', max_length=256, null=True)
    revenue = models.CharField('����(�鸸��)', max_length=256, null=True)
    info_company = models.TextField('ȸ��Ұ�', blank=True, null=True)
    info_biz = models.TextField('�ֿ���', blank=True, null=True)
    history = models.TextField('�ֿ��̷�', blank=True, null=True)
    deal = models.TextField('�ֿ�ŷ�ó', blank=True, null=True)
    category_middle = models.ManyToManyField(Develop, verbose_name='�Ƿڰ��ɺо�', related_name='category_middle')
    #possible_set = models.ManyToManyField(Subclass, verbose_name='���߰�����ǰ�о�', related_name='possible_product')
    history_set = models.ManyToManyField(Subclass, verbose_name='��������ǰ��', related_name='history_product')
    #����
    coin = models.IntegerField('����', default=2000, null=True)
    #ȸ������ �� ����
    file = models.FileField('ȸ��Ұ� �� ��������������', upload_to=partner_update_filename, blank=True, null=True)
    avg_score = models.DecimalField('�������', default=0, max_digits=5, decimal_places=2, null=True)
    # ��Ʈ�� ����
    #is_partner = models.BooleanField('��Ʈ�ʿ���', default=True, null=True)
    # ��Ʈ�� ���
    grade = models.IntegerField('��Ʈ�� ���', default=0, choices=PARTNER_GRADE, null=True)
    # �Ƚɹ�ȣ�� �ƴ� ���� ��ȭ��ȣ
    real_phone = models.CharField('���� �޴��� ��ȣ', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = '��Ʈ��'
        verbose_name_plural = '��Ʈ��'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Portfolio
# Description : ��Ʈ������ ��
# ------------------------------------------------------------------
class Portfolio(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    img_portfolio = models.ImageField('���������� �̹���', upload_to=portfolio_update_filename, null=True)
    is_main = models.BooleanField('���� ����', default=False)

    class Meta:
        verbose_name = '     ��Ʈ������'
        verbose_name_plural = '     ��Ʈ������'

    def __str__(self):
        return str(self.partner.name) + " ��Ʈ������"

# ------------------------------------------------------------------
# Model   : Structure
# Description : ������ ��
# ------------------------------------------------------------------
class Structure(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    img_structure = models.ImageField('������ �̹���', upload_to=structure_update_filename, null=True)
    is_main = models.BooleanField('���� ����', default=False)

    class Meta:
        verbose_name = '     ������'
        verbose_name_plural = '     ������'

    def __str__(self):
        return str(self.partner.name) + " ������"

# ------------------------------------------------------------------
# Model   : Machine
# Description : ������� ��
# ------------------------------------------------------------------
class Machine(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    img_machine = models.ImageField('������� �̹���', upload_to=machine_update_filename, null=True)
    is_main = models.BooleanField('���� ����', default=False)

    class Meta:
        verbose_name = '     �������'
        verbose_name_plural = '     �������'

    def __str__(self):
        return str(self.partner.name) + " �������"

# ------------------------------------------------------------------
# Model   : Certification
# Description : ��Ʈ������ ��
# ------------------------------------------------------------------
class Certification(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    img_certification = models.ImageField('���������� �̹���', upload_to=certification_update_filename, null=True)
    is_main = models.BooleanField('���� ����', default=False)

    class Meta:
        verbose_name = '     ����������'
        verbose_name_plural = '     ����������'

    def __str__(self):
        return str(self.partner.name) + " ����������"

# ------------------------------------------------------------------
# Model   : Process
# Description : ������� ��
# ------------------------------------------------------------------
class Process(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    img_process = models.ImageField('������� �̹���', upload_to=process_update_filename, null=True)
    is_main = models.BooleanField('���� ����', default=False)

    class Meta:
        verbose_name = '     �������'
        verbose_name_plural = '     �������'

    def __str__(self):
        return str(self.partner.name) + " �������"
        
# ------------------------------------------------------------------
# Model   : LoginLog
# Description : �α��� �α� ���� ��
# ------------------------------------------------------------------

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'User', null=True)
    created_at = models.DateTimeField('�α�������', auto_now_add=True)
    type = models.IntegerField('����Ÿ��', default=0, choices=USER_TYPE)


    class Meta:
        verbose_name = '�α��� �α�'
        verbose_name_plural = '�α��� �α�'
        ordering = ('-created_at',)

    def __str__(self):
        return '{}_log'.format(self.user)

class Path(models.Model):
    path = models.CharField('�湮���', max_length=256, null=True)


    class Meta:
        verbose_name = '�湮���'
        verbose_name_plural = '�湮���'

    def __str__(self):
        return str(self.path)

class Business(models.Model):
    business = models.CharField('����', max_length=256, null=True)


    class Meta:
        verbose_name = '����'
        verbose_name_plural = '����'

    def __str__(self):
        return str(self.business)
