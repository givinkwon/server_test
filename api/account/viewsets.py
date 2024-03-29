#-*- coding: cp949 -*-
from rest_framework import (
    viewsets,
    status,
    mixins,
)

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#pagenation
from .paginations import *

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.account.filters import *

import enum
from apps.utils import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate
from apps.account.models import *
from apps.category.models import *
from apps.kakaotalk.models import *
from .serializers import *

# 장고 메일 서버
from django.core.mail import EmailMessage

# logging
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# signal
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from django.db.models import F

class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1

class UserViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('username', in_=openapi.IN_QUERY,
                                                              description='아이디', type=openapi.TYPE_STRING),
                                            openapi.Parameter('password', in_=openapi.IN_QUERY,
                                                              description='비밀번호', type=openapi.TYPE_STRING),
                                            ], )
    @action(detail=False, methods=('POST',), url_path='login', http_method_names=('post',))
    def login(self, request, *args, **kawrgs):
        '''
        일반 로그인
        '''

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            
            LoginLog.objects.create(
                   user=user,
                   type=user.type,
            )
            
            if user.type == 0:
                client = Client.objects.filter(user=user)
                return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '로그인에 성공하였습니다.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Client' : ClientSerializer(client, many=True).data,
                                    }})
            partner = Partner.objects.filter(user=user)
            return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '로그인에 성공하였습니다.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Partner' : PartnerSerializer(partner, many=True).data,
                                    }})

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '아이디 혹은 비밀번호가 틀렸습니다.'},
        )

    @action(detail=False, methods=('POST',), url_path='data', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def Token_data(self, request, *args, **kawrgs):
        '''
        새로고침할 때, 토큰 보내서 데이터 가지고 오기
        '''
        user = request.user
        if user.type == 0:
            client = Client.objects.filter(user=user)
            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '클라이언트 데이터를 보내드립니다.',
                'data': {
                    'token': user.auth_token.key,
                    'User': PatchUserSerializer(user).data,
                    'Client': ClientSerializer(client, many=True).data,
                }})
        partner = Partner.objects.filter(user=user)
        return Response(data={
            'code': ResponseCode.SUCCESS.value,
            'message': '파트너 데이터를 보내드립니다.',
            'data': {
                'token': user.auth_token.key,
                'User': PatchUserSerializer(user).data,
                'Partner': PartnerSerializer(partner, many=True).data,
            }})


    @action(detail=False, methods=('PATCH',), url_path='deactivate', http_method_names=('patch',),  permission_classes=[IsAuthenticated], )
    def deactivate(self, request, *args, **kwargs):
        """
        회원 탈퇴
        """
        user = request.user
        password = request.data.get('password')
        if not authenticate(username=user.username, password=password):
            return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': '비밀번호가 맞지 않습니다.'},
                    )
        user.is_active = False
        user.save()

        return Response()
#    @swagger_auto_schema(request_body=openapi.Schema(
#        type=openapi.TYPE_OBJECT,
#        properties={
#            'phone_num': openapi.Schema(type=openapi.TYPE_STRING, description='핸드폰 번호'),
#        }
#    ), )
#    @action(detail=False, methods=('POST',), url_path='username', http_method_names=('post',))
#    def search_username(self, request, *args, **kwargs):
#        '''
#        아이디 찾기
#        '''
#        # if request.user.is_authenticated: 로그인시에는 true가 나옴
#        phone = request.data.get('phone')
#        user_qs = User.objects.filter(phone=phone)
#        if not user_qs.exists():
#            return Response(
#                        status=status.HTTP_400_BAD_REQUEST,
#                        data={'message': '해당 정보와 맞는 사용자가 없습니다.'},
#                    )

#        #email = EmailMessage('[볼트앤너트]아이디를 이메일로 보내드립니다.', '', to=[user_qs.first()])
#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'message' : '회원님의 이메일은 다음과 같습니다.',
#                              'data' : PatchUserSerializer(user_qs.first()).data,
#                             })

#   def search_password(self, request, *args, **kwargs): 추후 구현 예정

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                    properties={
                                        'password': openapi.Schema(type=openapi.TYPE_STRING, description='기존 비밀번호'),
                                        'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='새 비밀번호'),
                                    }, ),
    )
    @action(detail=False, methods=['PATCH', ], url_path='password',
            http_method_names=('patch',), permission_classes=(IsAuthenticated,), )
    def change_password(self, request, *args, **kwargs):
        '''
        비밀번호 변경
        '''
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = request.user
        if user.check_password(password):
            if password == new_password:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '이전과 같은 비밀번호를 입력하셨습니다.'}
                )
            user.set_password(new_password)
            user.save()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': '성공적으로 비밀번호를 변경하였습니다.'})
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '기존의 비밀번호가 맞지 않습니다.', })

    @action(detail=False, methods=('POST',), url_path='password/email', http_method_names=('post',))
    def send_password(self, request, *args, **kawrgs):
        username = request.data.get('username')
        phone = request.data.get('phone')
        user_qs = User.objects.filter(username=username, phone=phone)
        if user_qs.exists():
            user = User.objects.get(username=username, phone=phone)
            password = Util.get_random_letter(10)
            user.set_password(password)
            user.save()
            email = EmailMessage('[볼트앤너트]회원님의 임시 비밀번호를 이메일로 보내드립니다.', '회원님의 임시 비밀번호는\n\n' + password + '\n\n입니다.', to=[user.username])
            email.send()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message' : '임시 비밀번호가 회원님의 이메일로 발송되었습니다.',
                                  })
        return Response( status=status.HTTP_400_BAD_REQUEST,
                         data={'message': '회원정보가 올바르지 않습니다.'}
                                  )

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.filter(user__is_active=True)
        #.order_by('-date_joined')
    serializer_class = ClientSerializer
    pagination_class = ClientPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']

    @swagger_auto_schema(request_body=ClientSerializer)
    @action(detail=False, methods=('POST',), url_path='signup', http_method_names=('post',))
    def client_signup(self, request, *args, **kwargs):
        '''
        회원가입
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        title = request.data.get('title')
        path = request.data.get('path')
        business = request.data.get('business')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        # type에 따라서 def(partner / client)를 api를 따로 설계
        if not username or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '이메일 이나 비밀번호 값이 없습니다.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '전화번호 값이 없습니다.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 이메일이 이미 존재합니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=type,
            phone=phone,
            marketing=marketing,
        )

        client = Client.objects.create(
            user=user,
            name=name,
            title=title,
            path=path,
            business=business,
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '회원가입이 성공적으로 완료되었습니다.\n다시 로그인을 해주세요.',
                              'data': {
                                     'token': user.auth_token.key,
                                     'client': ClientSerializer(client).data,
                                     'user': PatchUserSerializer(user).data,
                                     # password가 없는 데이터를 보내줘야함
                                }})

    #@swagger_auto_schema(request_body=ClientSerializer)
    #@action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    #def kakao_client(self, request, *args, **kwargs):  # 클라이언트한테 제안서 등록될 때 카카오톡 보내기
    #    client = request.data.get('client')
    #    client_qs = Client.objects.filter(id=client)
    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
        # print(client_qs)
        # print(client_phone_list)
        # 리스트화
    #    client_phone_list = list(client_phone_list)
        # 공백제거
    #    client_phone_list = list(filter(None, client_phone_list))
        #print(client_phone_list)
        #response = kakaotalk_request.send(client_phone_list)
        #print(response)
        #Sendkakao.objects.create(
        #    status_code=response.status_code,
        #    description=response.json()['description'],
        #    refkey=response.json()['refkey'],
        #    messagekey=response.json()['messagekey'],
        #)
    #    return True
        #return Response(data={
        #    'code': ResponseCode.SUCCESS.value,
        #    'message': '발송에 성공하였습니다.',
        #    'data': {
        #        'status_code': response.status_code,
        #        'response': response.json(),
        #    }})


    #@action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    #@receiver(post_init, sender=Request)
    #def request_init(sender, instance, **kwargs):
    #    instance._previous_active_save = instance.active_save


    #@receiver(post_save, sender=Request)
    #def kakao_answer_end(sender, instance, **kwargs):
    #    client = instance.client.id
    #    client_qs = Client.objects.filter(id=client)
    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
    #    # 리스트화
    #    client_phone_list = list(client_phone_list)
    #    # 공백제거
    #    client_phone_list = list(filter(None, client_phone_list))
    #    # print(client_phone_list)

    #    if instance.active_save is False and instance._previous_active_save is True:
    #        response = kakaotalk_request.send(client_phone_list)
    #        print(response)
    #        Sendkakao.objects.create(
    #            status_code=response.status_code,
    #            description=response.json()['description'],
    #            refkey=response.json()['refkey'],
    #            messagekey=response.json()['messagekey'],
    #        )

    #        return Response(data={
    #            'code': ResponseCode.SUCCESS.value,
    #            'message': '발송에 성공하였습니다.',
    #            'data': {
    #                'status_code': response.status_code,
    #                'response': response.json(),
    #            }})

    #@action(detail=False, methods=('POST',), url_path='kakaotalk_meeting', http_method_names=('post',), )
    #@receiver(post_init, sender=Answer)
    #def answer_init(sender, instance, **kwargs):
    #    instance._previous_send_meeting = instance.send_meeting

    #@receiver(post_save, sender=Answer)
    #def kakao_answer_meeting(sender, instance, **kwargs):
    #    client = instance.client.id
    #    partner = instance.partner.id
    #    client_qs = Client.objects.filter(id=client)
    #    partner_qs = Partner.objects.filter(id=partner)

    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
    #    partner_phone_list = partner_qs.values_list('user__phone', flat=True)
    #    # 리스트화
    #    client_phone_list = list(client_phone_list)
    #    partner_phone_list = list(partner_phone_list)
    #    # 공백제거
    #    client_phone_list = list(filter(None, client_phone_list))
    #    partner_phone_list = list(filter(None, partner_phone_list))
    #    # print(client_phone_list)

    #    if instance.send_meeting is True and instance._previous_send_meeting is False:
    #        #response1 = kakaotalk_request.send(client_phone_list)
    #        #response2 = kakaotalk_request.send(partner_phone_list)


    #        #Sendkakao.objects.create(
    #        #    status_code=response1.status_code,
    #        #    description=response1.json()['description'],
    #        #    refkey=response1.json()['refkey'],
    #        #    messagekey=response1.json()['messagekey'],
    #        #)
    #        #Sendkakao.objects.create(
    #        #    status_code=response2.status_code,
    #        #    description=response2.json()['description'],
    #        #    refkey=response2.json()['refkey'],
    #        #    messagekey=response2.json()['messagekey'],
    #        #)

    #        return Response(data={
    #            'code': ResponseCode.SUCCESS.value,
    #            'message': '발송에 성공하였습니다.',
    #        #    'data': {
    #        #        'status_code': response1.status_code,
    #        #        'response': response1.json(),
    #        #    }
    #        })

    @action(detail=False, methods=('POST',), url_path='kakaotalk_send_information', http_method_names=('post',), )
    @receiver(post_init, sender=Request)
    def request_init(sender, instance, **kwargs):
        instance._previous_send_information = instance.send_information

    @receiver(post_save, sender=Request)
    def kakao_send_information(sender, instance, **kwargs):
        #client = instance.client.id
        project = instance.project.id
        #client_qs = Client.objects.filter(id=client)

        # answer information
        answer_qs = Answer.objects.filter(project=project)
        answer_list = answer_qs.values_list('partner',flat=True)
        answer_list = list(answer_list)

        partner_qs = Partner.objects.filter(id__in=answer_list)

        #client_phone_list = client_qs.values_list('user__phone', flat=True)
        partner_phone_list = partner_qs.values_list('real_phone', flat=True)
        # 리스트화
        #client_phone_list = list(client_phone_list)
        partner_phone_list = list(partner_phone_list)
        # 공백제거
        #client_phone_list = list(filter(None, client_phone_list))
        partner_phone_list = list(filter(None, partner_phone_list))

        # data
        subject = instance.name
        #print(subject)
        content = instance.content.replace("<p>","").replace("</p>","").replace("<br />","").replace("</br>","").replace("<br>","").replace("&nbsp;","")
        #if len(instance.content) != 0:
        #    content = instance.content.replace("<p>","").replace("</p>","")

        #print(content)
        price = instance.price
        #print(price)
        period = instance.day
        #print(period)
        file = "https://boltnnutplatform.s3.amazonaws.com/media/" + str(instance.file)
        #print(file)

        if instance.send_information is True and instance._previous_send_information is False:
            #print(client_phone_list)
            #print(partner_phone_list)
        #    response1 = kakaotalk_send_information.send(client_phone_list,subject, content, price, period, file)
            response2 = kakaotalk_send_information.send(partner_phone_list,subject, content, price, period, file)

            #Sendkakao.objects.create(
            #    status_code=response1.status_code,
            #    description=response1.json()['description'],
            #    refkey=response1.json()['refkey'],
            #    messagekey=response1.json()['messagekey'],
            #)
            Sendkakao.objects.create(
                status_code=response2.status_code,
                description=response2.json()['description'],
                refkey=response2.json()['refkey'],
                messagekey=response2.json()['messagekey'],
            )

            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '발송에 성공하였습니다.',
                'data': {
                    'status_code': response2.status_code,
                    'response': response2.json(),
                }
            })

class PartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    #orderbyList = ['-avg_score', '-id']
    queryset = Partner.objects.filter(user__is_active=True).order_by(F('grade').desc(nulls_last=True), F('avg_score').desc(nulls_last=True), F('id') , F('user__last_activity').desc(nulls_last=True))
    serializer_class = PartnerSerializer
    pagination_class = PartnerPageNumberPagination
    filter_backends = [filters.SearchFilter,PartnerFilter, filters.OrderingFilter]
    filterset_fields = ['history_set', 'city', 'region', 'category_middle__id', 'history_set__id']
    search_fields = ['name', 'info_company', 'info_biz', 'deal', 'history_set__subclass','category_middle__category']
    ordering_fields = '__all__'

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('POST',), url_path='signup',http_method_names=('post',))
    def partner_signup(self, request, *args, **kwargs):
        '''
        파트너 회원가입
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        
        name = request.data.get('name')
        logo = request.data.get('logo')
        city = request.data.get('city')
        region = request.data.get('region')
        career = request.data.get('career')
        employee = request.data.get('employee')
        revenue = request.data.get('revenue')
        info_company = request.data.get('info_company')
        info_biz = request.data.get('info_biz')
       # history = request.data.get('history')
        deal = request.data.get('deal')
        category_middle = request.data.get('category_middle')
        #possible_set = request.data.get('possible_set')
        history_set = request.data.get('history_set')

        # 리스트 형태로 받기 위해서
        category_middle = category_middle.split(',')
        #possible_set = possible_set.split(',')
        history_set = history_set.split(',')


        file = request.data.get('file')
        coin = 2000
        # type에 따라서 def(partner / client)를 api를 따로 설계
        if not name:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '상호명 값이 없습니다.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '연락처 값이 없습니다.'})

        if not logo:
             return Response(
                 status=status.HTTP_400_BAD_REQUEST,
                 data={'message': '로고 파일이 없습니다.'})

        if not career:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '경력 년수가 없습니다.'})

        if not employee:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '종업원 값이 없습니다.'})

        if not revenue:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '매출 값이 없습니다.'})

        if not info_company:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '회사소개 값이 없습니다.'})

        if not info_biz:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '주요사업 값이 없습니다.'})

     #   if not history:
     #       return Response(
     #           status=status.HTTP_400_BAD_REQUEST,
     #           data={'message': '연혁 값이 없습니다.'})

        if not deal:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '주요거래처 값이 없습니다.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 이메일이 이미 존재합니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=type,
            phone=phone,
            marketing=marketing,
        )

        partner = Partner.objects.create(
            user=user,
            name=name,
            career=career,
            employee=employee,
            revenue=revenue,
            info_company=info_company,
            info_biz=info_biz,
       #     history=history,
            deal=deal,
            coin=coin,
            logo=logo,
            file=file,
        )
        city = City.objects.filter(id=city)
        region=Region.objects.filter(id=region)
        partner.city = city.first()
        partner.region = region.first()

        category_elements = Develop.objects.filter(id__in=category_middle)
        history_elements = Subclass.objects.filter(id__in=history_set)
        #possible_elements = Subclass.objects.filter(id__in=possible_set)
        partner.category_middle.add(*category_elements)
        partner.history_set.add(*history_elements)
        #partner.possible_set.add(*possible_elements)
        partner.save()
        #form-data는 자동으로 주석 코드를 실행 시켜줌
        #serializer = PartnerSerializer(partner, data=request.data, partial=True)
        #serializer.is_valid(raise_exception=True)
        #instance = serializer.save()
        #instance.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '회원가입이 성공적으로 완료되었습니다.\n다시 로그인을 해주세요.',
                              'data': {
                                  'token': user.auth_token.key,
                                  'partner': PartnerSerializer(partner).data,
                                  'user': PatchUserSerializer(user).data,
                              }})

    # get_object는 튜플 하나인데, 필터가능, get_queryset 테이블 튜플 리스트인데 전체도 되고 필터도 가능
 # django filter로 대체
 #   @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def search(self, request, *args, **kwargs): # 파트너 검색용
 #       text = request.data.get('text')
 #       # __in은 list만 // text는 __icontains 이용
 #       result1 = Partner.objects.filter(name__icontains=text)
 #       result2 = Partner.objects.filter(info_company__icontains=text)
 #       result3 = Partner.objects.filter(info_biz__icontains=text)
 #       result4 = Partner.objects.filter(deal__icontains=text)
 #       # 제품군 검색을 일부로 안되게 만들기 >> 큐레이션을 이용할 수 있도록
 #       #추후에 유료 서비스로 개발 예정
 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '파트너 검색결과입니다.',
 #                             'data': PartnerSerializer(result1.union(result2).union(result3).union(result4), many=True).data
 #                             }
 #                       )

 #   @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def request_partner(self, request, *args, **kwargs):  # 의뢰서 보낼 파트너 정보 찾기
 #
 #       #maincategory = request.data.get('maincategory')
 #       #category = request.data.get('category')
 #
 #       subclass = request.data.get('subclass')
 #       #sub 클래스의 id를 보내야함.
 #
 #       possible_elements = Partner.objects.filter(possible_set__in=subclass)
 #       history_elements = Partner.objects.filter(history_set__in=subclass)

 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '의뢰서를 보낼 파트너 정보입니다.',
 #                             'data': PartnerSerializer(possible_elements.union(history_elements),many=True).data
 #                             }
 #                       )

 #   @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def region_search(self, request, *args, **kwargs):  # 지역에 따라 파트너 검색

 #       city = request.data.get('city') #시/도 id
 #       region = request.data.get('region') #구 id, 만약 시만 선택했을 때 리스트 형태의 id

 #       if not region: # 시/도만 고른 경우
 #           partner = Partner.objects.filter(city=city)
 #           return Response(data={'code': ResponseCode.SUCCESS.value,
 #                                 'message': '해당 지역의 파트너입니다.',
 #                                 'data': PartnerSerializer(partner, many=True).data
 #                                 }
 #                           )
 #       partner = Partner.objects.filter(region=region) #구를 고른 경우
 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '해당 지역의 파트너입니다.',
 #                             'data': PartnerSerializer(partner, many=True).data
 #                             }
 #                       )
    
 #    @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def category_search(self, request, *args, **kwargs):  # 의뢰 분야에 따른 파트너 검색용
 #
 #       category_big = request.data.get('category_big')  # 의뢰분야 대분류
 #       category_middle = request.data.get('category_middle')  # 의뢰분야 중분류

 #       if not category_middle:  # 의뢰분야 대분류만 고른경우
 #           partner = Partner.objects.filter(category_big__in=category_big)
 #           return Response(data={'code': ResponseCode.SUCCESS.value,
 #                                 'message': '해당 의뢰분야의 파트너입니다.',
 #                                 'data': PartnerSerializer(partner, many=True).data
 #                                 }
 #                           )
 #       partner = Partner.objects.filter(category_middle__in=category_middle)  # 의뢰분야 중분류를 고른 경우
 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '해당 의뢰분야의 파트너입니다.',
 #                             'data': PartnerSerializer(partner, many=True).data
 #                             }
 #                       )

   # @swagger_auto_schema(request_body=PartnerSerializer) # 추후 유료 서비스 개발
   # @action(detail=False, methods=('POST',), http_method_names=('post',))
   # def product_search(self, request, *args, **kwargs):  # 제품 분야에 따른 파트너 검색용 # 소분류 검색의 경우에는 나중에 추가 개발을 통해 유료 서비스화 진행 예정
   #
   #     product_big = request.data.get('product_big')  # 제품분야 대분류
   #     product = request.data.get('product')  # 제품분야 중분류
   #
   #     if not product:  # 제품분야 대분류만 고른경우
   #         partner = Partner.objects.filter(product_big__in=product_big)
   #         return Response(data={'code': ResponseCode.SUCCESS.value,
   #                               'message': '해당 지역의 파트너입니다.',
   #                               'data': PartnerSerializer(partner, many=True).data
   #                               }
   #                         )
   #     partner = Partner.objects.filter(product__in=product)  # 제품분야 중분류를 고른 경우
   #     return Response(data={'code': ResponseCode.SUCCESS.value,
   #                           'message': '해당 지역의 파트너입니다.',
   #                           'data': PartnerSerializer(partner, many=True).data
   #                           }
   #                     )

    @action(detail=False, methods=('GET',), url_path='request', http_method_names=('get',))
    def find_partner(self, request, *args, **kwargs):  # 의뢰서 완성 시에 적합한 파트너 리스트 추천
        subclass = request.GET['subclass']

       # partner1_qs = Partner.objects.filter(possible_set__id = subclass)
       # print(partner1_qs)
        partner2_qs = Partner.objects.filter(history_set__id = subclass)
       # print(partner2_qs)
        #query_set 합치기
       # partner_qs = partner1_qs.union(partner2_qs)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '해당 의뢰서에 적합한 파트너 리스트입니다.',
                              'data': PartnerSerializer(partner2_qs, many=True).data
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='coin', http_method_names=('patch',), permission_classes=(IsAuthenticated,),)
    def update_coin(self, request, *args, **kwargs):  # 코인을 결제했을 때 코인 추가
        # 결제 성공 시리얼을 받아서 아임포트에 요청.
        partner_id = request.user.partner.id
        #partner_id = request.data.get('partner_id')
        coin = request.data.get('coin')  # 프론트에서 Partner coin값을 불러와서 더하기 혹은 빼기 수행

        # filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        partner_data.coin += coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '코인을 업데이트한 파트너 정보입니다.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='minus-coin', http_method_names=('patch',),
            permission_classes=(IsAuthenticated,), )
    def minus_coin(self, request, *args, **kwargs):  # 결제 시에 코인을 빼주는 API
        # 결제 성공 시리얼을 받아서 아임포트에 요청.
        partner_id = request.user.partner.id
        coin = request.data.get('coin')  # 프론트에서 Partner coin값을 불러와서 더하기 혹은 빼기 수행

        # filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        partner_data.coin -= coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '코인을 업데이트한 파트너 정보입니다.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    #@swagger_auto_schema(request_body=PartnerSerializer)
    #@action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    #@receiver(post_init, sender=Request)
    #def request_init(sender, instance, **kwargs):
    #    instance._previous_examine = instance.examine

    #@receiver(post_save, sender=Request)
    #def request_kakaotalk(sender, instance, *args, **kwargs):  # 검수 시 적합한 파트너에게 카카오톡 알림
    #    client = instance.client
    #    subject = instance.name
    #    subclass = instance.product
    #    category = instance.category.values_list('category')
    #    category_list = list(category)
    #    # 리스트화
    #    for i in range(len(category_list)):
    #        category_list[i] = category_list[i][0]
    #    # print(category_list)
    #    # str 화
    #    category = "/".join(category_list)
    #    # print(category)
    #    if instance.examine == True and instance._previous_examine == False:
    #        list_partner = []
    #        for i in category_list:
    #            result = Partner.objects.filter(category_middle__category__contains=i)
    #            list_partner.append(result)
    #        partner_qs1 = list_partner[0]
    #        print(list_partner)
    #        for partner in list_partner:
    #            partner_qs_all = partner_qs1.union(partner)
    #        # query_set value 가져오기
    #        partner_phone_list = partner_qs_all.values_list('user__phone', flat=True)
    #        # 리스트화
    #        partner_phone_list = list(partner_phone_list)
    #        # 공백제거
    #        partner_phone_list = list(filter(None, partner_phone_list))
    #        print(partner_phone_list)
    #        ##response = kakaotalk2.send(partner_phone_list,subject, subclass, category)

    #        client_phone = User.objects.get(username = client.user).phone

            ##kakaotalk_request_edit_end.send(client_phone)
            #response = kakaotalk2.send(['010-4112-6637'], subject, subclass, category)
            ##Sendkakao.objects.create(
            ##    status_code=response.status_code,
            ##    description=response.json()['description'],
            ##    refkey=response.json()['refkey'],
            ##    messagekey=response.json()['messagekey'],
            ##)

            ##return Response(data={
            ##    'code': ResponseCode.SUCCESS.value,
            ##    'message': '발송에 성공하였습니다.',
            ##    'data': {
            ##        'status_code': response.status_code,
            ##        'response': response.json(),
            ##    }})
    #        return True
    #    return False

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='success', http_method_names=('patch',))
    def meeting_success(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        partner_data.success += 1
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '파트너 미팅 성공 횟수가 추가되었습니다.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='fail', http_method_names=('patch',))
    def meeting_fail(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        partner_data.fail += 1
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '파트너 미팅 실패 횟수가 추가되었습니다.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('GET',), url_path='meeting', http_method_names=('get',))
    def meeting_percent(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        meeting_count = (partner_data.success + partner_data.fail)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        if meeting_count == 0:
           if not partner_data.success == 0: # 미팅 성공이 1회 이상인 경우
                partner_data.meeting = 100
           else:                            # 미팅 성공이 0회인 경우
                partner_data.meeting = 0
        else:
            partner_data.meeting = partner_data.success / meeting_count

        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '파트너의 미팅 전환 성공율 입니다.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

class JustPartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    #orderbyList = ['-avg_score', '-id']
    queryset = Partner.objects.filter(user__is_active=True).order_by(F('grade').desc(nulls_last=True), F('avg_score').desc(nulls_last=True), F('id') , F('user__last_activity').desc(nulls_last=True))
    serializer_class = JustPartnerSerializer
    pagination_class = PartnerPageNumberPagination
    filter_backends = [filters.SearchFilter,PartnerFilter, filters.OrderingFilter]
    filterset_fields = ['history_set', 'city', 'region', 'category_middle__id', 'history_set__id']
    search_fields = ['name', 'info_company', 'info_biz', 'deal', 'history_set__subclass','category_middle__category']
    ordering_fields = '__all__'

class PortfolioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']

class StructureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']

class MachineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']

class CertificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']

class ProcessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']

class PathViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'path']

class BusinessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'business']


