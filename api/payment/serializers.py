from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.payment.models import *

class PaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paylist
        fields = ['id', 'merchant_uid', 'buyer_email','buyer_name','buyer_tel', 'state']




