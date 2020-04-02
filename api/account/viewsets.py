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
    queryset = Client.objects.all()
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

        phone = request.data.get('phone')
        type = request.data.get('type')

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
        )

        client = Client.objects.create(
            user=user,
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


class PartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    pagination_class = PartnerPageNumberPagination
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = ['possible_set', 'history_set', 'city', 'region', 'category_middle__id','possible_set__id', 'history_set__id']
    search_fields = ['name', 'info_company', 'info_biz', 'deal', 'possible_set__id', 'history_set__id']

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
        possible_set = request.data.get('possible_set')
        history_set = request.data.get('history_set')

        # 리스트 형태로 받기 위해서
        category_middle = category_middle.split(',')
        possible_set = possible_set.split(',')
        history_set = history_set.split(',')


        file = request.data.get('file')
        coin = 0
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

        user = User.objects.create_user(
            username=username,
            password=password,
            type=type,
            phone=phone,
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
        possible_elements = Subclass.objects.filter(id__in=possible_set)
        partner.category_middle.add(*category_elements)
        partner.history_set.add(*history_elements)
        partner.possible_set.add(*possible_elements)
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

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='coin', http_method_names=('patch',), permission_classes=(IsAuthenticated,),)
    def update_coin(self, request, *args, **kwargs):  # 코인을 결제했을 때 코인 추가 / 코인 사용 시 코인 감소
        # 결제 성공 시리얼을 받아서 아임포트에 요청.
        partner_id = request.user.partner.id
        #partner_id = request.data.get('partner_id')
        coin = request.data.get('coin')  # 프론트에서 Partner coin값을 불러와서 더하기 혹은 빼기 수행

        # filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
        partner_data = Partner.objects.get(id=partner_id)
        partner_data
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        partner_data.coin += coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '코인을 업데이트한 파트너 정보입니다.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    def request_kakaotalk(self, request, *args, **kwargs):  # 의뢰서 등록 시 적합한 파트너에게 카카오톡 알림
        subclass = request.data.get('subclass')
      #  print(Partner.objects.all().values_list('possible_set', flat=True))
      #  print(Partner.objects.filter(possible_set = "5"))
        partner_qs1 = Partner.objects.filter(possible_set = subclass)
        partner_qs2 = Partner.objects.filter(history_set = subclass)
        partner_qs_all = partner_qs1.union(partner_qs2)
        # query_set value 가져오기
        partner_phone_list = partner_qs_all.values_list('user__phone', flat=True)
        #리스트화
        partner_phone_list = list(partner_phone_list)

        response = kakaotalk.send(partner_phone_list)
        Sendkakao.objects.create(
            status_code=response.status_code,
            description=response.json()[description],
            refkey=response.json()[refkey],
            messagekey=response.json().messagekey[messagekey],
        )

        return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '발송에 성공하였습니다.',
                'data': {
                  'status_code': response.status_code,
                  'response': response.json(),
                }})

class PortfolioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class StructureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

class MachineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class CertificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

class ProcessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
#class GroupViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer
