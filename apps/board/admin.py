from django.contrib import admin
from django.db import models
from .models import *

from typing import TYPE_CHECKING

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'is_top', 'created_at']

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'is_top', 'created_at', 'link']