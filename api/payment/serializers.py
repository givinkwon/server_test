from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.payment.models import *

class PaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paylist
        fields = ['id','user', 'merchant_uid', 'status', 'product_price', 'coin', 'channel', 'pay_method' ]




