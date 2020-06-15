from django.contrib import admin
from django.db import models
from apps.project.models import *
from apps.account.models import *


class ReviewInline(admin.StackedInline):
    model = Review
    can_delete = True
    extra = 0
    max_num = 15


class RequestInline(admin.StackedInline):
    model = Request
    can_delete = True
    extra = 0
    max_num = 15


class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = True
    extra = 0
    max_num = 15


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [RequestInline, AnswerInline,ReviewInline]
    list_display = ['request_name','client_phone','client_email','project_price','project_created','count_answer','count_meeting']
    
    def request_name(self, obj):
        project_id = obj.id
        request_name = Request.objects.get(project = project_id)
        return request_name

    def client_email(self, obj):
        project_id = obj.id
        client = Request.objects.get(project=project_id).client
        return client
        
    def client_phone(self, obj):
        project_id = obj.id
        client = Request.objects.get(project=project_id).client
        phone = User.objects.get(username=client).phone
        return phone

    def project_price(self, obj):
        project_id = obj.id
        request_price = Request.objects.get(project=project_id).price
        return request_price

    def project_created(self, obj):
        project_id = obj.id
        created_at = Request.objects.get(project=project_id).created_at
        return created_at

    def count_answer(self, obj):
        project_id = obj.id
        answer = Answer.objects.filter(project=project_id)
        count = len(answer)
        return count

    def count_meeting(self, obj):
        project_id = obj.id
        answer_yes = Answer.objects.filter(project = project_id, state = 1)
        count = len(answer_yes)
        return count
      
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'created_at', 'id', 'project', 'name', 'price', 'day']

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
    list_display = ['created_at', 'id', 'project', 'all_price', 'day','state','file']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'project', 'partner']
