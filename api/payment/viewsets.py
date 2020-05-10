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

#iamport
from iamport import Iamport
import requests as rq



"""
프론트앤드 작업자 분이 요청하신 ORDER API는 merchant_uid 생성을 위한 API입니다.
따라서 payment에 대한 모델을 만드신 후 model.id + @로 고유한 merchant_uid를 생성하셔야 합니다.(generate_muid 참조)
PAYMENTAPI는 결제 진행 후 검증용으로 이용하시면 될 것 같습니다.

## ORDERAPI - Iamport 이용할 필요 없음
1. ORDERAPI 작성
2. ORDERAPI 에서는 비어있는 payment 모델을 생성
3. payment 모델에 muid 필드(CharField, 256정도, 원하시는 길이로 생성하시면 됩니다.)를 생성하신 후 모델 id를 바탕으로 muid를 생성하여 저장
4. ORDERAPI의 응답으로 {code:......., mid: 모델id, muid: 모델muid} 반환

## PAYMENTAPI
1. 클라이언트로부터 merchant_uid 및 결제 정보를 입력받음
2. iamp.find 혹은 iamp.findall로 결제 정보 검색
3. 클라이언트가 보낸 정보(merchant_uid, amount, 카드정보등등...)이 일치한다면 정상 코드 전송
4. 일치하지 않는다면 취소 요청 후 에러 코드 전송
"""

def generate_random_code(length=5):
    from random import choices
    CODE='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    weight = [1] * len(CODE)
    return ''.join(choices(CODE, weight, k=length))

def generate_muid(mid, prefix = 'boltnnut'):
    return f'{prefix}__{generate_random_code()}__{mid:010d}'

###############################################################################

class PaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Paylist.objects.all()
    serializer_class = PaylistSerializer

    @swagger_auto_schema(request_body=PaylistSerializer)
    @action(detail=False, methods=('POST',), url_path='order', http_method_names=('post',),permission_classes=(IsAuthenticated,),)
    def order(self, request, *args, **kwargs):  # merchant_uid를 저장하고 해쉬화
        user = request.user
        product_name = request.data.get('product_name') # 상품명
        product_price = request.data.get('product_price')
        coin = request.data.get('coin')
        # merchant_uid hash화
        merchant_hash = generate_muid(user.id)
        paylist = Paylist.objects.create(
                                 user=user,
                                 merchant_uid=merchant_hash,
                                 product_name = product_name,
                                 product_price = product_price,
                                 coin = coin,
                                 status = 0,
                                 channel = 0,
                                 pay_method = 0,
                             )
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '결제 리스트입니다.',
                              'data': {
                                    'paylist' : PaylistSerializer(paylist).data,
                                  }})

    @swagger_auto_schema(request_body=PaylistSerializer)
    @action(detail=False, methods=('POST',), url_path='payment', http_method_names=('post',),permission_classes=(IsAuthenticated,),)
    def payment(self, request, *args, **kwargs):  # 결제 확인
            date = request.data.get('date')
            user = request.user
            merchant_uid = request.data.get('merchant_uid')
            #print(-1)
            product_price = Paylist.objects.get(merchant_uid = merchant_uid).product_price
            #print(0)
            print(product_price)
            #product_price = request.data.get('product_price')
            # 아임포트 인스턴스 가져오기
            iamport = Iamport(imp_key=settings.IAMPORT_KEY, imp_secret=settings.IAMPORT_SECRET)
            response = iamport.find(merchant_uid=merchant_uid)
            print(response)
            if response:
              #  print(1)
                if iamport.is_paid(int(product_price), response=response):
              #      print(2)
                    paylist = Paylist.objects.get(merchant_uid=merchant_uid)
                   # print(paylist)
                    paylist.status = response['status']
                    paylist.channel = response['channel']
                    paylist.pay_method = response['pay_method']
                    paylist.save()
                #    print(paylist)
                    if date:
                        a , _ = Clientclass.objects.get_or_create(
                            client = user.client
                        )
                        a.end_time = date
                        a.client_class = 1
                        a.save()

                    return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '결제가 성공적으로 완료되었습니다.',
                              'data': {
                                    'paylist' : PaylistSerializer(paylist).data,
                                  }})

                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': '비정상적인 결제 요청입니다. (결제 금액이 다릅니다.)'}
                                       )

            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': '비정상적인 결제 요청입니다.(결제정보가 없습니다.)'}
                                 )

         #   if iamport:
         #       print(iamport.find(merchant_uid="1"))
         #       response = iamport.find(merchant_uid=merchant_uid)  # 결제정보 가져오기
         #       if response:
         #           print(response)
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



   #         return Response(status=status.HTTP_400_BAD_REQUEST,
   #                         data={'message': '아임포트 Key가 잘못되었습니다.'}
   #                         )

   #     return Response(status=status.HTTP_400_BAD_REQUEST,
   #                     data={'message': '결제가 실패되었습니다.'}
   #                     )
