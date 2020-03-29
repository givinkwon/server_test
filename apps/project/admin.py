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
    list_display = ['id']

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'created_at', 'id', 'project', 'name', 'price', 'day']

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
    list_display = ['created_at', 'id', 'project', 'price', 'day','state']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'project', 'partner']
