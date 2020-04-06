from rest_framework import (
    viewsets,
    status,
    mixins,
)

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
# pagenation
from .paginations import *

# django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

import enum
from apps.utils import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.payment.models import *
from .serializers import *
from iamport import Iamport
from django.conf import settings
from hashids import Hashids
import hashlib

class PaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Paylist.objects.all()
    serializer_class = PaylistSerializer

    @swagger_auto_schema(request_body=PaylistSerializer)
    @action(detail=False, methods=('POST',), url_path='merchant', http_method_names=('post',),permission_classes=(IsAuthenticated,),)
    def save_merchant(self, request, *args, **kwargs):  # merchant_uid를 저장하고 해쉬화
        merchant_uid = request.data.get('merchant_uid')
        user = request.user
        # merchant_uid hash화
        m = hashlib.md5()
        m.update(merchant_uid.encode('utf-8'))
        merchant_hash = m.hexdigest()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '결제가 성공적으로 완료되었습니다.',
                              'data': {
                                    'merchant_hash' : merchant_hash,
                                    'paylist' : PaylistSerializer(paylist).data,
                                  }})
    @swagger_auto_schema(request_body=PaylistSerializer)
    @action(detail=False, methods=('POST',), url_path='payment', http_method_names=('post',),)
    def payment(self, request, *args, **kwargs):  # 결제 확인
            iamport = Iamport(imp_key=settings.IAMPORT_KEY, imp_secret=settings.IAMPORT_SECRET)  # 아임포트 인스턴스 가져오기
            if iamport:
                print(iamport.find(merchant_uid="1"))
                response = iamport.find(merchant_uid=merchant_uid)  # 결제정보 가져오기
                if response:
                    print(response)
   #                 iamport.is_paid(product_price, merchant_uid=merchant_uid)  # 결제 가격이랑 들어온 데이터 비교하기
   #                 if iamport.is_paid:
   #                     paylist = Paylist.objects.create(
   #                         user=user,
   #                         merchant_uid=merchant_uid,
   #                         state=state,
   #                         product_price=product_price,
   #                         coin=coin,
   #                     )

   #                     return Response(data={'code': ResponseCode.SUCCESS.value,
   #                                           'message': '결제가 성공적으로 완료되었습니다.',
   #                                           'data': {
   #                                               'iamport': iamport,
   #                                               'paylist': PaylistSerializer(paylist).data,
   #                                           }})

   #                 return Response(status=status.HTTP_400_BAD_REQUEST,
   #                                 data={'message': '비정상적인 결제 요청입니다. (결제 금액이 다릅니다.'}
   #                                 )

   #             return Response(status=status.HTTP_400_BAD_REQUEST,
   #                             data={'message': '비정상적인 결제 요청입니다.(결제정보가 없습니다.)'}
   #                             )

   #         return Response(status=status.HTTP_400_BAD_REQUEST,
   #                         data={'message': '아임포트 Key가 잘못되었습니다.'}
   #                         )

   #     return Response(status=status.HTTP_400_BAD_REQUEST,
   #                     data={'message': '결제가 실패되었습니다.'}
   #                     )
