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
                data = data['region'].split(',')
                return queryset.filter(region__in=data)

          elif 'city' in data_dict:
                   data = data['city'].split(',')
                   return queryset.filter(city__in=data)

          elif 'category_middle__id' in data_dict:
                   data = data['category_middle__id'].split(',')
                   return queryset.filter(category_middle__in=data)

        #  elif 'possible_set' in data_dict:
        #           data = data['possible_set'].split(',')
        #           return queryset.filter(category_middle__in=data)

          elif 'possible_set__id' in data_dict:
                   data = data['possible_set__id'].split(',')
                   return queryset.filter(possible_set__in=data)

        #  elif 'history_set' in data_dict:
        #           data = data['history_set'].split(',')
        #           return queryset.filter(category_middle__in=data)

          elif 'history_set__id' in data_dict:
                   data = data['history_set__id'].split(',')
                   return queryset.filter(history_set__in=data)

          return queryset.filter()