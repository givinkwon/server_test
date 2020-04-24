import django_filters
from rest_framework import filters
from django.db.models import (
    Case,
    Count,
    When,
)

from apps.account.models import *

class PartnerFilter(filters.BaseFilterBackend): # 파라미터 여러 개 보내도 or로 가져오는 필터

        def filter_queryset(self, request, queryset, view):  ## 필터 부를 때 자동
          data=request.GET
          data_dict = data.dict() # dictionary 화

          if  'region' in data_dict:
                data2 = data['region'].split(',')
                queryset = queryset.filter(region__in=data2).distinct('id')

          if 'city' in data_dict:
                data2 = data['city'].split(',')
                queryset = queryset.filter(city__in=data2).distinct('id')

          if 'category_middle__id' in data_dict:
                data2 = data['category_middle__id'].split(',')
                queryset = queryset.filter(category_middle__in=data2).distinct('id')

          if 'possible_set__id' in data_dict:
                data2 = data['possible_set__id'].split(',')
                queryset = queryset.filter(possible_set__in=data2).distinct('id')

          if 'history_set__id' in data_dict:
                data2 = data['history_set__id'].split(',')
                queryset = queryset.filter(history_set__in=data2).distinct('id')

          return queryset
