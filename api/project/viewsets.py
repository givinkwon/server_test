from apps.project.models import *
from apps.category.models import *
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
#count
from django.db.models import Count

import enum

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate
from apps.account.models import *
from apps.category.models import *

# filter
from apps.project.filters import RequestFilter

from .serializers import *
from api.category.serializers import *

class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1

class RequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    pagination_class = RequestPageNumberPagination
    filter_backends = [RequestFilter,filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['client__id', 'project__id', 'product__id']

    def perform_create(self, serializer):
        project = Project.objects.create()
        serializer.save(project=project.id)
        print(serializer)

   # search_fields = []
# 장고 필터로 대체
#    @swagger_auto_schema(request_body=RequestSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_request(self, request, *args, **kwargs):  # 요청한 의뢰서 확인(유저기준)
#
#        user = request.data.get('user')
#        # user id

#        request = Request.objects.filter(user=user)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': RequestSerializer(request, many=True).data
#                              })

#    @swagger_auto_schema(request_body=RequestSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_request_project(self, request, *args, **kwargs):  # 프로젝트마다 의뢰서 찾아오기
#
#        project = request.data.get('project')
#        # project id

#        request = Request.objects.filter(project=project)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': RequestSerializer(request, many=True).data
#                              })


    @swagger_auto_schema(request_body=RequestSerializer)
    @action(detail=False, methods=('POST',), url_path='partner', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def find_request_partner(self, request, *args, **kwargs):  # 파트너에게 적합한 문의서 모두 가져오기
        possible_product = request.user.partner.possible_set
        history_prodcut = request.user.partner.history_set
        #print(possible_product)

        #subclass_qs
        request1_qs = possible_product.all()
        request2_qs = history_prodcut.all()
        #query_set 합치기
        partner_product = request1_qs.union(request2_qs)
        #query_set value 가져오기
        partner_product = partner_product.values_list('id', flat=True)
        request = Request.objects.filter(product__in=partner_product)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '해당 파트너에게 적합한 모든 문의서입니다.',
                              'data': RequestSerializer(request, many=True).data
                              }
                        )


class SelectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Select.objects.all()
    serializer_class = SelectSerializer
    filter_backends = [DjangoFilterBackend]
    # filters.SearchFilter]
    filterset_fields = ['category__id']

    # search_fields = []

    @swagger_auto_schema(request_body=SelectSerializer)
    @action(detail=False, methods=('POST',), url_path='category', http_method_names=('post',))
    def find_select(self, request, *args, **kwargs):  # 선택된 개발 분야에 따라 선택질문 선별

        category = request.data.get('category')
        # product id

        develop_instances = Develop.objects.filter(id__in=category)
       # select = Select.objects.filter(range__in=product_instances)
    #    select = Select.objects.filter(range=product) # 왜 둘 다 되지..?

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': DevelopSerializer(develop_instances, many=True).data
                              })

class CommonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Common.objects.all()
    serializer_class = CommonSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    orderbyList = ['-partner__avg_score', 'id']
    queryset = Answer.objects.all().order_by(*orderbyList)
    serializer_class = AnswerSerializer
    pagination_class = AnswerPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    # filters.SearchFilter]
    filterset_fields = ['project__id', 'partner__id']

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('POST',), url_path='first-active', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def first_active(self, request, *args, **kwargs):  # 제일 평점 높은 파트너 활성화 > 프로젝트마다 되어야함.
            project__id = request.data.get('project__id')
            answer_qs = Answer.objects.filter(project = project__id)
            if answer_qs.exists():
                instance=answer_qs.first()
                instance.active = True
                instance.save()
                return Response(data={'code': ResponseCode.SUCCESS.value,
                                      'message' : "평점이 제일 높은 파트너가 활성화되었습니다.",
                                      'data': AnswerSerializer(answer_qs, many=True).data
                                    })
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "프로젝트에 들어온 제안서가 없습니다"
                            })

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='active', http_method_names=('patch',))
    def change_active(self, request, *args, **kwargs):  # 파트너의 id를 받아서 해당 id의 파트너가 보낸 제안서의 active 값을 True로 만들어주는 API
        partner_id = request.data.get('partner_id')
        project_id = request.data.get('project_id')
        answer_qs = Answer.objects.filter(project = project_id, partner = partner_id)
        print(answer_qs)
        if answer_qs.exists():
            instance = answer_qs.first()
            instance.active = True
            instance.save()
            print(instance)
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': "해당 파트너의 제안서가 활성화되었습니다."
                                  })
        return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "프로젝트에 들어온 제안서가 없습니다"
                            })
    # search_fields = []
#장고 필터로 대체
#    @swagger_auto_schema(request_body=AnswerSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_answer(self, request, *args, **kwargs):  # 해당 프로젝트에 제안한 파트너 정보와 제안서 확인

#        project = request.data.get('project')
#        # project id

#        answer = Answer.objects.filter(project=project)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': AnswerSerializer(answer, many=True).data
#                              })

#    @swagger_auto_schema(request_body=AnswerSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_answer_partner(self, request, *args, **kwargs):  # 파트너가 쓴 모든 제안서 불러오기

#        partner = request.data.get('partner')
#        # partner id

#        answer = Answer.objects.filter(partner=partner)
#        print(answer)
#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': AnswerSerializer(answer, many=True).data
#                              })

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    # filters.SearchFilter]
    filterset_fields = ['project__id',  'partner__id']

    @swagger_auto_schema(request_body=ReviewSerializer)
    @action(detail=False, methods=['POST', ], url_path='create', http_method_names=('post',),)
    def create_review(self, request, *args, **kwargs):  #리뷰를 만드는 api
        client = request.data.get('client')
        project = request.data.get('project')
        partner = request.data.get('partner')
        price_score = request.data.get('price_score')
        time_score = request.data.get('time_score')
        talk_score = request.data.get('talk_score')
        expert_score = request.data.get('expert_score')
        result_score = request.data.get('result_score')
        content = request.data.get('content')

        review = Review.objects.create(
            client=client,
            project=project,
            partner=partner,
            price_score=price_score,
            time_score=time_score,
            talk_score=talk_score,
            expert_score=expert_score,
            result_score=result_score,
            content=content,
        )

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': ReviewSerializer(review).data
                              })

    #    @swagger_auto_schema(request_body=ReviewSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def score_avg(self, request, *args, **kwargs):  # 파트너 평점 불러오기 >> Serializer로 옮김
#
#        partner = request.data.get('partner')
#        #partner id
#
#        a = Review.objects.filter(partner=partner).aggregate(Avg('price_score'))
#        b = Review.objects.filter(partner=partner).aggregate(Avg('time_score'))
#        c = Review.objects.filter(partner=partner).aggregate(Avg('talk_score'))
#        d = Review.objects.filter(partner=partner).aggregate(Avg('expert_score'))
#        e = Review.objects.filter(partner=partner).aggregate(Avg('result_score'))

#        avg_score = (a['price_score__avg'] + b['time_score__avg'] + c['talk_score__avg'] + d['expert_score__avg'] + e['result_score__avg']) / 5

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'message': '해당 파트너 평점입니다',
#                              'data': avg_score
#                              }
#                        )

#    @swagger_auto_schema(request_body=ReviewSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def review_partner(self, request, *args, **kwargs):  # 파트너 리뷰 리스트 가져오기

#        partner = request.data.get('partner')
#        # partner id

#        review = Review.objects.filter(partner=partner)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'message': '해당 파트너 리뷰입니다',
#                              'data': ReviewSerializer(review,many=True).data
#                              }
#                        )

#    @swagger_auto_schema(request_body=ReviewSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_review_project(self, request, *args, **kwargs):  # 프로젝트마다 파트너 리뷰 찾아오기

#        project = request.data.get('project')
        # project id

#        review = Review.objects.filter(project=project)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': ReviewSerializer(review, many=True).data
#                              })

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Project.objects.annotate(answer_count = Count('answer')).order_by('answer_count')
    serializer_class = ProjectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    @swagger_auto_schema(request_body=ProjectSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='state', http_method_names=('patch',))
    def change_state(self, request, *args, **kwargs):  # 버튼 클릭에 따라 프로젝트 state 상태를 바꾸는 api

        project_id = request.data.get('project_id')
        state = request.data.get('state')
        # project id

        #filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
        update_project = Project.objects.get(id=project_id)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        serializer = ProjectSerializer(update_project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': ProjectSerializer(update_project).data
                              })
