from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.board.models import *

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['url', 'title', 'content', 'is_top', 'created_at']

class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = ['url', 'title', 'image', 'is_top', 'created_at', 'link']