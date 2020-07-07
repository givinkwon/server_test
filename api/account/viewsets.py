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

# ��� ���� ����
from django.core.mail import EmailMessage

# logging
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# signal
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

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
                                                              description='���̵�', type=openapi.TYPE_STRING),
                                            openapi.Parameter('password', in_=openapi.IN_QUERY,
                                                              description='��й�ȣ', type=openapi.TYPE_STRING),
                                            ], )
    @action(detail=False, methods=('POST',), url_path='login', http_method_names=('post',))
    def login(self, request, *args, **kawrgs):
        '''
        �Ϲ� �α���
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
                                    'message': '�α��ο� �����Ͽ����ϴ�.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Client' : ClientSerializer(client, many=True).data,
                                    }})
            partner = Partner.objects.filter(user=user)
            return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '�α��ο� �����Ͽ����ϴ�.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Partner' : PartnerSerializer(partner, many=True).data,
                                    }})

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '���̵� Ȥ�� ��й�ȣ�� Ʋ�Ƚ��ϴ�.'},
        )

    @action(detail=False, methods=('POST',), url_path='data', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def Token_data(self, request, *args, **kawrgs):
        '''
        ���ΰ�ħ�� ��, ��ū ������ ������ ������ ����
        '''
        user = request.user
        if user.type == 0:
            client = Client.objects.filter(user=user)
            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': 'Ŭ���̾�Ʈ �����͸� �����帳�ϴ�.',
                'data': {
                    'token': user.auth_token.key,
                    'User': PatchUserSerializer(user).data,
                    'Client': ClientSerializer(client, many=True).data,
                }})
        partner = Partner.objects.filter(user=user)
        return Response(data={
            'code': ResponseCode.SUCCESS.value,
            'message': '��Ʈ�� �����͸� �����帳�ϴ�.',
            'data': {
                'token': user.auth_token.key,
                'User': PatchUserSerializer(user).data,
                'Partner': PartnerSerializer(partner, many=True).data,
            }})


    @action(detail=False, methods=('PATCH',), url_path='deactivate', http_method_names=('patch',),  permission_classes=[IsAuthenticated], )
    def deactivate(self, request, *args, **kwargs):
        """
        ȸ�� Ż��
        """
        user = request.user
        password = request.data.get('password')
        if not authenticate(username=user.username, password=password):
            return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': '��й�ȣ�� ���� �ʽ��ϴ�.'},
                    )
        user.is_active = False
        user.save()

        return Response()
#    @swagger_auto_schema(request_body=openapi.Schema(
#        type=openapi.TYPE_OBJECT,
#        properties={
#            'phone_num': openapi.Schema(type=openapi.TYPE_STRING, description='�ڵ��� ��ȣ'),
#        }
#    ), )
#    @action(detail=False, methods=('POST',), url_path='username', http_method_names=('post',))
#    def search_username(self, request, *args, **kwargs):
#        '''
#        ���̵� ã��
#        '''
#        # if request.user.is_authenticated: �α��νÿ��� true�� ����
#        phone = request.data.get('phone')
#        user_qs = User.objects.filter(phone=phone)
#        if not user_qs.exists():
#            return Response(
#                        status=status.HTTP_400_BAD_REQUEST,
#                        data={'message': '�ش� ������ �´� ����ڰ� �����ϴ�.'},
#                    )

#        #email = EmailMessage('[��Ʈ�س�Ʈ]���̵� �̸��Ϸ� �����帳�ϴ�.', '', to=[user_qs.first()])
#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'message' : 'ȸ������ �̸����� ������ �����ϴ�.',
#                              'data' : PatchUserSerializer(user_qs.first()).data,
#                             })

#   def search_password(self, request, *args, **kwargs): ���� ���� ����

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                    properties={
                                        'password': openapi.Schema(type=openapi.TYPE_STRING, description='���� ��й�ȣ'),
                                        'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='�� ��й�ȣ'),
                                    }, ),
    )
    @action(detail=False, methods=['PATCH', ], url_path='password',
            http_method_names=('patch',), permission_classes=(IsAuthenticated,), )
    def change_password(self, request, *args, **kwargs):
        '''
        ��й�ȣ ����
        '''
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = request.user
        if user.check_password(password):
            if password == new_password:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '������ ���� ��й�ȣ�� �Է��ϼ̽��ϴ�.'}
                )
            user.set_password(new_password)
            user.save()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': '���������� ��й�ȣ�� �����Ͽ����ϴ�.'})
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '������ ��й�ȣ�� ���� �ʽ��ϴ�.', })

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
            email = EmailMessage('[��Ʈ�س�Ʈ]ȸ������ �ӽ� ��й�ȣ�� �̸��Ϸ� �����帳�ϴ�.', 'ȸ������ �ӽ� ��й�ȣ��\n\n' + password + '\n\n�Դϴ�.', to=[user.username])
            email.send()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message' : '�ӽ� ��й�ȣ�� ȸ������ �̸��Ϸ� �߼۵Ǿ����ϴ�.',
                                  })
        return Response( status=status.HTTP_400_BAD_REQUEST,
                         data={'message': 'ȸ�������� �ùٸ��� �ʽ��ϴ�.'}
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
        ȸ������
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        title = request.data.get('title')
        path = request.data.get('path')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        # type�� ���� def(partner / client)�� api�� ���� ����
        if not username or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�̸��� �̳� ��й�ȣ ���� �����ϴ�.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '��ȭ��ȣ ���� �����ϴ�.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ش� �̸����� �̹� �����մϴ�.'})

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
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': 'ȸ�������� ���������� �Ϸ�Ǿ����ϴ�.\n�ٽ� �α����� ���ּ���.',
                              'data': {
                                     'token': user.auth_token.key,
                                     'client': ClientSerializer(client).data,
                                     'user': PatchUserSerializer(user).data,
                                     # password�� ���� �����͸� ���������
                                }})

    @swagger_auto_schema(request_body=ClientSerializer)
    @action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    def kakao_client(self, request, *args, **kwargs):  # Ŭ���̾�Ʈ���� ���ȼ� ��ϵ� �� īī���� ������
        client = request.data.get('client')
        client_qs = Client.objects.filter(id=client)
        client_phone_list = client_qs.values_list('user__phone', flat=True)
        # print(client_qs)
        # print(client_phone_list)
        # ����Ʈȭ
        client_phone_list = list(client_phone_list)
        # ��������
        client_phone_list = list(filter(None, client_phone_list))
        #print(client_phone_list)
        response = kakaotalk_request.send(client_phone_list)
        print(response)
        Sendkakao.objects.create(
            status_code=response.status_code,
            description=response.json()['description'],
            refkey=response.json()['refkey'],
            messagekey=response.json()['messagekey'],
        )

        return Response(data={
            'code': ResponseCode.SUCCESS.value,
            'message': '�߼ۿ� �����Ͽ����ϴ�.',
            'data': {
                'status_code': response.status_code,
                'response': response.json(),
            }})


    @action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    @receiver(post_init, sender=Request)
    def request_init(sender, instance, **kwargs):
        instance._previous_active_save = instance.active_save


    @receiver(post_save, sender=Request)
    def kakao_answer_end(sender, instance, **kwargs):
        client = instance.client.id
        client_qs = Client.objects.filter(id=client)
        client_phone_list = client_qs.values_list('user__phone', flat=True)
        # ����Ʈȭ
        client_phone_list = list(client_phone_list)
        # ��������
        client_phone_list = list(filter(None, client_phone_list))
        # print(client_phone_list)

        if instance.active_save is False and instance._previous_active_save is True:
            response = kakaotalk_request.send(client_phone_list)
            print(response)
            Sendkakao.objects.create(
                status_code=response.status_code,
                description=response.json()['description'],
                refkey=response.json()['refkey'],
                messagekey=response.json()['messagekey'],
            )

            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '�߼ۿ� �����Ͽ����ϴ�.',
                'data': {
                    'status_code': response.status_code,
                    'response': response.json(),
                }})

    @action(detail=False, methods=('POST',), url_path='kakaotalk_meeting', http_method_names=('post',), )
    @receiver(post_init, sender=Answer)
    def answer_init(sender, instance, **kwargs):
        instance._previous_send_meeting = instance.send_meeting

    @receiver(post_save, sender=Answer)
    def kakao_answer_meeting(sender, instance, **kwargs):
        client = instance.client.id
        partner = instance.partner.id
        client_qs = Client.objects.filter(id=client)
        partner_qs = Partner.objects.filter(id=partner)

        client_phone_list = client_qs.values_list('user__phone', flat=True)
        partner_phone_list = partner_qs.values_list('user__phone', flat=True)
        # ����Ʈȭ
        client_phone_list = list(client_phone_list)
        partner_phone_list = list(partner_phone_list)
        # ��������
        client_phone_list = list(filter(None, client_phone_list))
        partner_phone_list = list(filter(None, partner_phone_list))
        # print(client_phone_list)

        if instance.send_meeting is True and instance._previous_send_meeting is False:
            #response1 = kakaotalk_request.send(client_phone_list)
            #response2 = kakaotalk_request.send(partner_phone_list)


            #Sendkakao.objects.create(
            #    status_code=response1.status_code,
            #    description=response1.json()['description'],
            #    refkey=response1.json()['refkey'],
            #    messagekey=response1.json()['messagekey'],
            #)
            #Sendkakao.objects.create(
            #    status_code=response2.status_code,
            #    description=response2.json()['description'],
            #    refkey=response2.json()['refkey'],
            #    messagekey=response2.json()['messagekey'],
            #)

            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '�߼ۿ� �����Ͽ����ϴ�.',
            #    'data': {
            #        'status_code': response1.status_code,
            #        'response': response1.json(),
            #    }
            })

class PartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    orderbyList = ['-avg_score','-login_count', 'id']
    queryset = Partner.objects.filter(user__is_active=True).annotate(login_count = Count('user__loginlog')).order_by(*orderbyList)
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
        ��Ʈ�� ȸ������
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

        # ����Ʈ ���·� �ޱ� ���ؼ�
        category_middle = category_middle.split(',')
        #possible_set = possible_set.split(',')
        history_set = history_set.split(',')


        file = request.data.get('file')
        coin = 2000
        # type�� ���� def(partner / client)�� api�� ���� ����
        if not name:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '��ȣ�� ���� �����ϴ�.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '����ó ���� �����ϴ�.'})

        if not logo:
             return Response(
                 status=status.HTTP_400_BAD_REQUEST,
                 data={'message': '�ΰ� ������ �����ϴ�.'})

        if not career:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '��� ����� �����ϴ�.'})

        if not employee:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '������ ���� �����ϴ�.'})

        if not revenue:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '���� ���� �����ϴ�.'})

        if not info_company:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'ȸ��Ұ� ���� �����ϴ�.'})

        if not info_biz:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ֿ��� ���� �����ϴ�.'})

     #   if not history:
     #       return Response(
     #           status=status.HTTP_400_BAD_REQUEST,
     #           data={'message': '���� ���� �����ϴ�.'})

        if not deal:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ֿ�ŷ�ó ���� �����ϴ�.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ش� �̸����� �̹� �����մϴ�.'})

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
        #form-data�� �ڵ����� �ּ� �ڵ带 ���� ������
        #serializer = PartnerSerializer(partner, data=request.data, partial=True)
        #serializer.is_valid(raise_exception=True)
        #instance = serializer.save()
        #instance.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': 'ȸ�������� ���������� �Ϸ�Ǿ����ϴ�.\n�ٽ� �α����� ���ּ���.',
                              'data': {
                                  'token': user.auth_token.key,
                                  'partner': PartnerSerializer(partner).data,
                                  'user': PatchUserSerializer(user).data,
                              }})

    # get_object�� Ʃ�� �ϳ��ε�, ���Ͱ���, get_queryset ���̺� Ʃ�� ����Ʈ�ε� ��ü�� �ǰ� ���͵� ����
 # django filter�� ��ü
 #   @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def search(self, request, *args, **kwargs): # ��Ʈ�� �˻���
 #       text = request.data.get('text')
 #       # __in�� list�� // text�� __icontains �̿�
 #       result1 = Partner.objects.filter(name__icontains=text)
 #       result2 = Partner.objects.filter(info_company__icontains=text)
 #       result3 = Partner.objects.filter(info_biz__icontains=text)
 #       result4 = Partner.objects.filter(deal__icontains=text)
 #       # ��ǰ�� �˻��� �Ϻη� �ȵǰ� ����� >> ť���̼��� �̿��� �� �ֵ���
 #       #���Ŀ� ���� ���񽺷� ���� ����
 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '��Ʈ�� �˻�����Դϴ�.',
 #                             'data': PartnerSerializer(result1.union(result2).union(result3).union(result4), many=True).data
 #                             }
 #                       )

 #   @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def request_partner(self, request, *args, **kwargs):  # �Ƿڼ� ���� ��Ʈ�� ���� ã��
 #
 #       #maincategory = request.data.get('maincategory')
 #       #category = request.data.get('category')
 #
 #       subclass = request.data.get('subclass')
 #       #sub Ŭ������ id�� ��������.
 #
 #       possible_elements = Partner.objects.filter(possible_set__in=subclass)
 #       history_elements = Partner.objects.filter(history_set__in=subclass)

 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '�Ƿڼ��� ���� ��Ʈ�� �����Դϴ�.',
 #                             'data': PartnerSerializer(possible_elements.union(history_elements),many=True).data
 #                             }
 #                       )

 #   @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def region_search(self, request, *args, **kwargs):  # ������ ���� ��Ʈ�� �˻�

 #       city = request.data.get('city') #��/�� id
 #       region = request.data.get('region') #�� id, ���� �ø� �������� �� ����Ʈ ������ id

 #       if not region: # ��/���� �� ���
 #           partner = Partner.objects.filter(city=city)
 #           return Response(data={'code': ResponseCode.SUCCESS.value,
 #                                 'message': '�ش� ������ ��Ʈ���Դϴ�.',
 #                                 'data': PartnerSerializer(partner, many=True).data
 #                                 }
 #                           )
 #       partner = Partner.objects.filter(region=region) #���� �� ���
 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '�ش� ������ ��Ʈ���Դϴ�.',
 #                             'data': PartnerSerializer(partner, many=True).data
 #                             }
 #                       )
    
 #    @swagger_auto_schema(request_body=PartnerSerializer)
 #   @action(detail=False, methods=('POST',), http_method_names=('post',))
 #   def category_search(self, request, *args, **kwargs):  # �Ƿ� �о߿� ���� ��Ʈ�� �˻���
 #
 #       category_big = request.data.get('category_big')  # �Ƿںо� ��з�
 #       category_middle = request.data.get('category_middle')  # �Ƿںо� �ߺз�

 #       if not category_middle:  # �Ƿںо� ��з��� �����
 #           partner = Partner.objects.filter(category_big__in=category_big)
 #           return Response(data={'code': ResponseCode.SUCCESS.value,
 #                                 'message': '�ش� �Ƿںо��� ��Ʈ���Դϴ�.',
 #                                 'data': PartnerSerializer(partner, many=True).data
 #                                 }
 #                           )
 #       partner = Partner.objects.filter(category_middle__in=category_middle)  # �Ƿںо� �ߺз��� �� ���
 #       return Response(data={'code': ResponseCode.SUCCESS.value,
 #                             'message': '�ش� �Ƿںо��� ��Ʈ���Դϴ�.',
 #                             'data': PartnerSerializer(partner, many=True).data
 #                             }
 #                       )

   # @swagger_auto_schema(request_body=PartnerSerializer) # ���� ���� ���� ����
   # @action(detail=False, methods=('POST',), http_method_names=('post',))
   # def product_search(self, request, *args, **kwargs):  # ��ǰ �о߿� ���� ��Ʈ�� �˻��� # �Һз� �˻��� ��쿡�� ���߿� �߰� ������ ���� ���� ����ȭ ���� ����
   #
   #     product_big = request.data.get('product_big')  # ��ǰ�о� ��з�
   #     product = request.data.get('product')  # ��ǰ�о� �ߺз�
   #
   #     if not product:  # ��ǰ�о� ��з��� �����
   #         partner = Partner.objects.filter(product_big__in=product_big)
   #         return Response(data={'code': ResponseCode.SUCCESS.value,
   #                               'message': '�ش� ������ ��Ʈ���Դϴ�.',
   #                               'data': PartnerSerializer(partner, many=True).data
   #                               }
   #                         )
   #     partner = Partner.objects.filter(product__in=product)  # ��ǰ�о� �ߺз��� �� ���
   #     return Response(data={'code': ResponseCode.SUCCESS.value,
   #                           'message': '�ش� ������ ��Ʈ���Դϴ�.',
   #                           'data': PartnerSerializer(partner, many=True).data
   #                           }
   #                     )

    @action(detail=False, methods=('GET',), url_path='request', http_method_names=('get',))
    def find_partner(self, request, *args, **kwargs):  # �Ƿڼ� �ϼ� �ÿ� ������ ��Ʈ�� ����Ʈ ��õ
        subclass = request.GET['subclass']

       # partner1_qs = Partner.objects.filter(possible_set__id = subclass)
       # print(partner1_qs)
        partner2_qs = Partner.objects.filter(history_set__id = subclass)
       # print(partner2_qs)
        #query_set ��ġ��
       # partner_qs = partner1_qs.union(partner2_qs)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '�ش� �Ƿڼ��� ������ ��Ʈ�� ����Ʈ�Դϴ�.',
                              'data': PartnerSerializer(partner2_qs[:5], many=True).data
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='coin', http_method_names=('patch',), permission_classes=(IsAuthenticated,),)
    def update_coin(self, request, *args, **kwargs):  # ������ �������� �� ���� �߰�
        # ���� ���� �ø����� �޾Ƽ� ������Ʈ�� ��û.
        partner_id = request.user.partner.id
        #partner_id = request.data.get('partner_id')
        coin = request.data.get('coin')  # ����Ʈ���� Partner coin���� �ҷ��ͼ� ���ϱ� Ȥ�� ���� ����

        # filter�� �˻� �� Queryset�� ��, get�� ���� �������� ������ ���ܸ� �߻���Ŵ
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.coin += coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '������ ������Ʈ�� ��Ʈ�� �����Դϴ�.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='minus-coin', http_method_names=('patch',),
            permission_classes=(IsAuthenticated,), )
    def minus_coin(self, request, *args, **kwargs):  # ���� �ÿ� ������ ���ִ� API
        # ���� ���� �ø����� �޾Ƽ� ������Ʈ�� ��û.
        partner_id = request.user.partner.id
        coin = request.data.get('coin')  # ����Ʈ���� Partner coin���� �ҷ��ͼ� ���ϱ� Ȥ�� ���� ����

        # filter�� �˻� �� Queryset�� ��, get�� ���� �������� ������ ���ܸ� �߻���Ŵ
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.coin -= coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '������ ������Ʈ�� ��Ʈ�� �����Դϴ�.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    @receiver(post_init, sender=Request)
    def request_init(sender, instance, **kwargs):
        instance._previous_examine = instance.examine

    @receiver(post_save, sender=Request)
    def request_kakaotalk(sender, instance, *args, **kwargs):  # �˼� �� ������ ��Ʈ�ʿ��� īī���� �˸�
        client = instance.client
        subject = instance.name
        subclass = instance.product
        category = instance.category.values_list('category')
        category_list = list(category)
        # ����Ʈȭ
        for i in range(len(category_list)):
            category_list[i] = category_list[i][0]
        # print(category_list)
        # str ȭ
        category = "/".join(category_list)
        # print(category)
        if instance.examine == True and instance._previous_examine == False:
            list_partner = []
            for i in category_list:
                result = Partner.objects.filter(category_middle__category__contains=i)
                list_partner.append(result)
            partner_qs1 = list_partner[0]
            print(list_partner)
            for partner in list_partner:
                partner_qs_all = partner_qs1.union(partner)
            # query_set value ��������
            partner_phone_list = partner_qs_all.values_list('user__phone', flat=True)
            # ����Ʈȭ
            partner_phone_list = list(partner_phone_list)
            # ��������
            partner_phone_list = list(filter(None, partner_phone_list))
            print(partner_phone_list)
            response = kakaotalk2.send(partner_phone_list,subject, subclass, category)

            client_phone = User.objects.get(username = client.user).phone

            kakaotalk_request_edit_end.send(client_phone)
            #response = kakaotalk2.send(['010-4112-6637'], subject, subclass, category)
            Sendkakao.objects.create(
                status_code=response.status_code,
                description=response.json()['description'],
                refkey=response.json()['refkey'],
                messagekey=response.json()['messagekey'],
            )

            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '�߼ۿ� �����Ͽ����ϴ�.',
                'data': {
                    'status_code': response.status_code,
                    'response': response.json(),
                }})
        return False

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='success', http_method_names=('patch',))
    def meeting_success(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.success += 1
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '��Ʈ�� ���� ���� Ƚ���� �߰��Ǿ����ϴ�.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='fail', http_method_names=('patch',))
    def meeting_fail(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.fail += 1
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '��Ʈ�� ���� ���� Ƚ���� �߰��Ǿ����ϴ�.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('GET',), url_path='meeting', http_method_names=('get',))
    def meeting_percent(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        meeting_count = (partner_data.success + partner_data.fail)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        if meeting_count == 0:
           if not partner_data.success == 0: # ���� ������ 1ȸ �̻��� ���
                partner_data.meeting = 100
           else:                            # ���� ������ 0ȸ�� ���
                partner_data.meeting = 0
        else:
            partner_data.meeting = partner_data.success / meeting_count

        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '��Ʈ���� ���� ��ȯ ������ �Դϴ�.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

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


