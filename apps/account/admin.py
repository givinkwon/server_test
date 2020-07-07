#-*- coding: cp949 -*-
from django.contrib import admin

from .models import *
from apps.project.models import *
# Register your models here.

from django.forms import TextInput, Textarea
from django.db import models

from typing import TYPE_CHECKING

import csv
from django.http import HttpResponse


class PortfolioInline(admin.StackedInline):
    model = Portfolio
    can_delete = True
    extra = 0
    max_num = 15

class StructureInline(admin.StackedInline):
    model = Structure
    can_delete = True
    extra = 0
    max_num = 15

class MachineInline(admin.StackedInline):
    model = Machine
    can_delete = True
    extra = 0
    max_num = 15

class CertificationInline(admin.StackedInline):
    model = Certification
    can_delete = True
    extra = 0
    max_num = 15

class ProcessInline(admin.StackedInline):
    model = Process
    can_delete = True
    extra = 0
    max_num = 15

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id','username', 'date_joined','type', 'partner_name', 'phone','marketing']
    actions = ['export_as_csv']

    def partner_name(self, obj):
        if(obj.type == 1):
            partner_name = Partner.objects.get(user=obj.id).name
            return partner_name


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','client_phone', 'client_email', 'name', 'title','path', 'marketing','client_signup_date',
                        'request_count', 'latest_request', 'answer_count', 'meeting_count']
    actions = ['export_as_csv']
    def client_phone(self, obj):
        phone = User.objects.get(username=obj.user).phone
        return phone

    def client_email(self, obj):
        email = User.objects.get(username=obj.user).username
        return email

    def marketing(self, obj):
        marketing = User.objects.get(username=obj.user).marketing
        if marketing ==True:
            return 'O'
        return 'X'

    def client_signup_date(self, obj):
        return obj.user.date_joined

        client_signup_date.short_descrption = "��������"

    def request_count(self, obj):
        request = Request.objects.filter(client=obj)
        count = len(request)
        return count

        request_count.short_descrption = "�Ƿڼ� ��"

    def latest_request(self, obj):
        request = Request.objects.filter(client=obj).order_by('-created_at')
        latest_request = request.first()
        return latest_request

        latest_request.short_descrption = "�ֱ� �Ƿ�"

    def answer_count(self, obj):
        answer = Answer.objects.filter(client=obj)
        count = len(answer)
        return count

        answer_count.short_descrption = "���ȼ� ��"

    def meeting_count(self, obj):
        answer = Answer.objects.filter(client=obj, state=1)
        count = len(answer)
        return count

        meeting_count.short_descrption = "���� �� Ƚ��"

@admin.register(Clientclass)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'client']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    inlines = [PortfolioInline, StructureInline, MachineInline, CertificationInline, ProcessInline]
    list_display = ['id', 'partner_phone', 'partner_email', 'name', 'city']

    def partner_phone(self, obj):
        phone = User.objects.get(username=obj.user).phone
        return phone

    def partner_email(self, obj):
        email = User.objects.get(username=obj.user).username
        return email


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['id','user','type','created_at']

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ['id','path']
