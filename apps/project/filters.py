import django_filters
from rest_framework import filters
from django.db.models import (
    Case,
    Count,
    When,
)

from apps.project.models import *

class RequestFilter(filters.BaseFilterBackend): # 파라미터 여러 개 보내도 or로 가져오는 필터

        def filter_queryset(self, request, queryset, view):  ## 필터 부를 때 자동
          data=request.GET
          data_dict = data.dict() # dictionary 화

          if  'product__id' in data_dict:
                data = data['product__id'].split(',')
                return queryset.filter(product__in=data)

          elif 'client__id' in data_dict:
                   data = data['client__id'].split(',')
                   return queryset.filter(client__in=data)

          return queryset.filter()