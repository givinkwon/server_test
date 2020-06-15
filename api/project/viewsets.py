#-*- coding: cp949 -*-
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

from apps.utils import *

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
        serializer.save(project=project)
        

   # search_fields = []
# ��� ���ͷ� ��ü
#    @swagger_auto_schema(request_body=RequestSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_request(self, request, *args, **kwargs):  # ��û�� �Ƿڼ� Ȯ��(��������)
#
#        user = request.data.get('user')
#        # user id

#        request = Request.objects.filter(user=user)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': RequestSerializer(request, many=True).data
#                              })

#    @swagger_auto_schema(request_body=RequestSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_request_project(self, request, *args, **kwargs):  # ������Ʈ���� �Ƿڼ� ã�ƿ���
#
#        project = request.data.get('project')
#        # project id

#        request = Request.objects.filter(project=project)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': RequestSerializer(request, many=True).data
#                              })


    @swagger_auto_schema(request_body=RequestSerializer)
    @action(detail=False, methods=('POST',), url_path='partner', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def find_request_partner(self, request, *args, **kwargs):  # ��Ʈ�ʿ��� ������ ���Ǽ� ��� ��������
        possible_product = request.user.partner.possible_set
        history_prodcut = request.user.partner.history_set
        #print(possible_product)

        #subclass_qs
        request1_qs = possible_product.all()
        request2_qs = history_prodcut.all()
        #query_set ��ġ��
        partner_product = request1_qs.union(request2_qs)
        #query_set value ��������
        partner_product = partner_product.values_list('id', flat=True)
        request = Request.objects.filter(product__in=partner_product)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '�ش� ��Ʈ�ʿ��� ������ ��� ���Ǽ��Դϴ�.',
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
    def find_select(self, request, *args, **kwargs):  # ���õ� ���� �о߿� ���� �������� ����

        category = request.data.get('category')
        # product id

        develop_instances = Develop.objects.filter(id__in=category)
       # select = Select.objects.filter(range__in=product_instances)
    #    select = Select.objects.filter(range=product) # �� �� �� ����..?

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': DevelopSerializer(develop_instances, many=True).data
                              })

class Select_saveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Select_save.objects.all()
    serializer_class = Select_saveSerializer
    filter_backends = [DjangoFilterBackend]
    # filters.SearchFilter]
    filterset_fields = ['request','category']

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
    orderbyList = ['-partner__avg_score', '-partner__meeting','id']
    queryset = Answer.objects.all().order_by(*orderbyList)
    serializer_class = AnswerSerializer
    pagination_class = AnswerPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filters.SearchFilter]
    filterset_fields = ['project__id', 'partner__id', 'state']
    ordering_fields = '__all__'

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('POST',), url_path='first-active', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def first_active(self, request, *args, **kwargs):  # ���� ���� ���� ��Ʈ�� Ȱ��ȭ > ������Ʈ���� �Ǿ����.
            project__id = request.data.get('project__id')
            answer_qs = Answer.objects.filter(project = project__id)
            if answer_qs.exists():
                instance=answer_qs.first()
                instance.active = True
                instance.save()
                return Response(data={'code': ResponseCode.SUCCESS.value,
                                      'message' : "������ ���� ���� ��Ʈ�ʰ� Ȱ��ȭ�Ǿ����ϴ�.",
                                      'data': AnswerSerializer(answer_qs, many=True).data
                                    })
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "������Ʈ�� ���� ���ȼ��� �����ϴ�"
                            })

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='active', http_method_names=('patch',))
    def change_active(self, request, *args, **kwargs):  # ��Ʈ���� id�� �޾Ƽ� �ش� id�� ��Ʈ�ʰ� ���� ���ȼ��� active ���� True�� ������ִ� API
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
                                  'message': "�ش� ��Ʈ���� ���ȼ��� Ȱ��ȭ�Ǿ����ϴ�."
                                  })
        return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "������Ʈ�� ���� ���ȼ��� �����ϴ�"
                            })
    # search_fields = []
#��� ���ͷ� ��ü
#    @swagger_auto_schema(request_body=AnswerSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_answer(self, request, *args, **kwargs):  # �ش� ������Ʈ�� ������ ��Ʈ�� ������ ���ȼ� Ȯ��

#        project = request.data.get('project')
#        # project id

#        answer = Answer.objects.filter(project=project)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'data': AnswerSerializer(answer, many=True).data
#                              })

#    @swagger_auto_schema(request_body=AnswerSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_answer_partner(self, request, *args, **kwargs):  # ��Ʈ�ʰ� �� ��� ���ȼ� �ҷ�����

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
    filterset_fields = ['project__id',  'partner__id', 'id']

    @swagger_auto_schema(request_body=ReviewSerializer)
    @action(detail=False, methods=['POST', ], url_path='create', http_method_names=('post',),)
    def create_review(self, request, *args, **kwargs):  #���並 ����� api
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
#    def score_avg(self, request, *args, **kwargs):  # ��Ʈ�� ���� �ҷ����� >> Serializer�� �ű�
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
#                              'message': '�ش� ��Ʈ�� �����Դϴ�',
#                              'data': avg_score
#                              }
#                        )

#    @swagger_auto_schema(request_body=ReviewSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def review_partner(self, request, *args, **kwargs):  # ��Ʈ�� ���� ����Ʈ ��������

#        partner = request.data.get('partner')
#        # partner id

#        review = Review.objects.filter(partner=partner)

#        return Response(data={'code': ResponseCode.SUCCESS.value,
#                              'message': '�ش� ��Ʈ�� �����Դϴ�',
#                              'data': ReviewSerializer(review,many=True).data
#                              }
#                        )

#    @swagger_auto_schema(request_body=ReviewSerializer)
#    @action(detail=False, methods=('POST',), http_method_names=('post',))
#    def find_review_project(self, request, *args, **kwargs):  # ������Ʈ���� ��Ʈ�� ���� ã�ƿ���

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
    def change_state(self, request, *args, **kwargs):  # ��ư Ŭ���� ���� ������Ʈ state ���¸� �ٲٴ� api

        project_id = request.data.get('project_id')
        state = request.data.get('state')
        # project id

        #filter�� �˻� �� Queryset�� ��, get�� ���� �������� ������ ���ܸ� �߻���Ŵ
        update_project = Project.objects.get(id=project_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        serializer = ProjectSerializer(update_project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': ProjectSerializer(update_project).data
                              })
