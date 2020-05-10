from django.contrib import admin

from .models import *
# Register your models here.

from django.forms import TextInput, Textarea
from django.db import models

from typing import TYPE_CHECKING

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

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'password','type', 'phone']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Clientclass)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'client']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    inlines = [PortfolioInline, StructureInline, MachineInline, CertificationInline, ProcessInline]
    list_display = ['id', 'name', 'city']



