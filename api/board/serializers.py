from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.board.models import *

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'is_top', 'created_at']

class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = ['id', 'title', 'content', 'image', 'is_top', 'created_at']