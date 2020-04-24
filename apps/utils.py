from django.utils.deconstruct import deconstructible

from rest_framework.response import Response
import datetime
import os
import random
import string
import uuid
import enum
import requests
import json
import time
class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1


@deconstructible
class FilenameChanger(object):

    def __init__(self, base_path):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.base_path = '{}/{}'.format(base_path, str(date))

    def __call__(self, instance, filename, *args, **kwargs):
        ext = filename.split('.')[-1].lower()
        filename = "%s.%s" % (uuid.uuid4(), ext)
        path = os.path.join(self.base_path, filename)
        print('[File] Upload File')
        print('- name : {}'.format(filename))
        print('- format : {}'.format(ext))
        print('- new name : {}'.format(filename))
        print('- path : {}'.format(path))
        return path

    def __eq__(self, other):
        return self.base_path


@deconstructible
class Util():

    @classmethod
    def add_unit(cls, value):
        UNIT = (
            (100000000, 'B'),
            (1000000, 'M'),
            (1000, 'K'),
            (1, ''),
        )
        for count, unit in UNIT:
            if value % count != value:
                number = round(value / count, 1)
                if (number*10)%10 == 0:
                    number = int(number)
                return '{number}{unit}'.format(number=str(number), unit=unit)
        return '{number}{unit}'.format(number=value, unit='')

    @classmethod
    def get_random_digit_letter(cls, length):
        result = ''
        for i in range(length):
            result += random.choice(string.digits)
        return str(result)

    @classmethod
    def get_random_letter(cls, length):
        result = ''
        for i in range(length):
            result += random.choice(string.digits + string.ascii_letters)
        return str(result)

class kakaotalk(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list):
            print(phone_list)
            for phone in phone_list:
             print(phone)
             url = 'https://api.bizppurio.com/v1/message'
             data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
                     'to': phone, 'content': {
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
             time.sleep(5)
             response = requests.post(url, data=json.dumps(data), headers=headers)
            return response


class kakaotalk_request(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list):
            print(phone_list)
            for phone in phone_list:
             #print(phone)
             url = 'https://api.bizppurio.com/v1/message'
             data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
                     'to': phone, 'content': {
                   'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'answer_to_client',
                            'message': '고객님의 의뢰에 대한 전문가의 제안서가 도착하였습니다.',

                          'button': [
                                {
                                 'name': '확인하러 가기',
                                 'type': 'WL',
                                 'url_mobile': 'http://www.boltnnut.com',
                                 'url_pc': 'http://www.boltnnut.com'
                             }
                         ]}}}
             headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
             time.sleep(5)
             response = requests.post(url, data=json.dumps(data), headers=headers)
            return response
