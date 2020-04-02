from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.payment.models import *
from apps.kakaotalk.models import *

class SendkakaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sendkakao
        fields = ['id', 'status_code', 'description', 'refkey', 'messagekey']
