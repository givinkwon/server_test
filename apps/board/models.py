#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

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

def magazine_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "magazine/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_magazine" + "." + ext
    return os.path.join(path, format)


# ------------------------------------------------------------------
# Model   : Notice
# Description : �������� ��
# ------------------------------------------------------------------
class Notice(models.Model):

    title = models.CharField('����', max_length=40)
    content = RichTextUploadingField(blank=True, null=True)
    is_top = models.BooleanField('��ܰ�������', default=False)
    created_at = models.DateTimeField('�������', auto_now_add=True)

    class Meta:
        verbose_name = '   �Խñ�'
        verbose_name_plural = '   �Խñ�'

    def __str__(self):
        return str(self.title) + " : �Խñ�"


# ------------------------------------------------------------------
# Model   : Magazine
# Description : �Ű��� ��
# ------------------------------------------------------------------
class Magazine(models.Model):

    title = models.CharField('����', max_length=40)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField('�Ű��� �̹���', upload_to=magazine_update_filename, null=True)
    is_top = models.BooleanField('��ܰ�������', default=False)
    created_at = models.DateTimeField('�������', auto_now_add=True)
    #link = models.CharField('��ũ', max_length=300)

    class Meta:
        verbose_name = '   �Ű���'
        verbose_name_plural = '   �Ű���'

    def __str__(self):
        return str(self.title) + " : �Ű���"