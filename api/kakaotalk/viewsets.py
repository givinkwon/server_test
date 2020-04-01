from apps.payment.models import *
from rest_framework import viewsets
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
#-*- coding: utf-8 -*-

import requests
import json

class KakaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    @action(detail=False, methods=('POST',), url_path='kakao', http_method_names=('post',))
    def kakao(self, request, *args, **kwargs):
        url = 'https://api.bizppurio.com/v1/message'
        data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
                'to': '01041126637', 'content': {
                'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner',
                       'message': '파트너님에게 적합한 의뢰서가 도착했습니다.',

                       'button': [
                           {
                               'name': '확인하러 가기',
                               'type': 'WL',
                               'url_mobile': 'http://www.boltnnut.com',
                               'url_pc': 'http://www.boltnnut.com'
                           }
                       ]}}}

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print("Status code: ", response.status_code)
        print("Printing Entire Post Request")
        print(response.json())