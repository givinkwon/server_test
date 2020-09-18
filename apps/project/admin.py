from django.contrib import admin
from django.db import models
from apps.project.models import *
from apps.account.models import *
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm
import logging


class ReviewInline(admin.StackedInline):
    model = Review
    can_delete = True
    extra = 0
    max_num = 15

#class RequestInlineFormset(BaseInlineFormSet):
#     def get_queryset(self):
#        qs = super(RequestInlineFormset, self).get_queryset()
#        print(qs)
#        return qs

class RequestInline(admin.StackedInline):
    model = Request
    can_delete = True
    readonly_fields = ['client', 'product', 'category']
    #exclude = ['price', 'day']
    extra = 0
    max_num = 15
    #formset = RequestInlineFormset


class ProjectInline(admin.StackedInline):
    model = Answer
    can_delete = True
    #formset = AnswerInlineFormset

#class AnswerInlineFormset(BaseInlineFormSet):
#    def get_queryset(self):
#        qs = super(AnswerInlineFormset, self).get_queryset()
#        print(qs)
#        return qs.select_related('partner')

class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = True
    raw_id_fields = ("partner",)
    #autocomplete_fields = ['partner__user']
    fields = ['client','partner', 'open_time', 'send_meeting', 'info_check','active']
    extra = 0
    max_num = 20

class QuestionInline(admin.TabularInline):
    model = Select_save
    can_delete = True
    extra = 0
    max_num = 15

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [RequestInline,AnswerInline]
    list_display = ['request_id', 'request_name', 'client_email','client_phone', 'project_created','count_answer','count_meeting','answer_status']

    #def name(self, obj):
    #    return obj.name

    #def client(self, obj):
    #    return client

    #def created_at(self, obj):
    #    return created_at

    #def get_queryset(self, request):
    #    queryset = Request.objects.select_related('project')
    #    return queryset

    ##
    request_queryset = Request.objects.all().select_related('client', 'client__user')
    answer_queryset = Answer.objects.all()

    def request_id(self, obj):
        project_id = obj.id
        request_id = self.request_queryset.get(project = project_id).id
        return request_id

    def request_name(self, obj):
        project_id = obj.id
        request = self.request_queryset.get(project = project_id)

        return request

    def client_email(self, obj):
        project_id = obj.id
        client = self.request_queryset.get(project=project_id).client
        return client

    def client_phone(self, obj):
        project_id = obj.id
        client = self.request_queryset.get(project=project_id).client
        phone = User.objects.get(username=client).phone
        return phone


    def project_created(self, obj):
        project_id = obj.id
        created_at = self.request_queryset.get(project=project_id).created_at
        return created_at

    def count_answer(self, obj):
        project_id = obj.id
        answer = self.answer_queryset.filter(project=project_id)
        count = len(answer)
        return count

    def count_meeting(self, obj):
        project_id = obj.id
        answer_yes = self.answer_queryset.filter(project = project_id, state = 1)
        count = len(answer_yes)
        return count

    def answer_status(self, obj):
        project_id = obj.id
        answer = self.answer_queryset.filter(project = project_id, info_check =1)
        count = len(answer)
        return count

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'created_at', 'name']# 'target_select']
    inlines = [QuestionInline]

    #def target_select(self, obj):
    #    request = obj
    #    select_qs = Select_save.objects.filter(request = request)
    #    answer_list = select_qs.values_list('question', 'answer')

    #    answer = list(answer_list)
    #    list_qus = []

    #    try:
    #        for answer in answer_list:
    #            qus = answer[0] + ":" + answer[1]
    #            list_qus.append(qus)
    #        return list_qus
    #    except:
    #        return "X"

@admin.register(Select_save)
class Select_saveAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'request', 'question', 'answer']

@admin.register(Select)
class SelectAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'request']

@admin.register(Content)
class SelectAdmin(admin.ModelAdmin):
    list_display = ['id', 'request', 'content1', 'content2', 'content3', 'content4']

@admin.register(Common)
class CommonAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'price', 'day', 'content','file']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['partner_phone', 'created_at', 'request_name', 'all_price', 'day','state','file', 'partner']


    def partner_phone(self, obj):
        partner = obj.partner
        phone = User.objects.get(username=partner).phone
        return phone

    def request_name(self, obj):
        project_id = obj.project
        request_name = Request.objects.get(project = project_id)
        return request_name

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'project', 'partner']
