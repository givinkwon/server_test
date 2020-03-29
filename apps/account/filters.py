import django_filters
from rest_framework import filters
from django.db.models import (
    Case,
    Count,
    When,
)

from apps.account.models import *

class PartnerFilter(filters.SearchFilter):

    name = django_filters.CharFilter(label='업체명', field_name='name', lookup_expr='icontains', )
    info_company = django_filters.CharFilter(label='회사소개', field_name='info_company', lookup_expr='icontains', )
    info_biz = django_filters.CharFilter(label='주요사업', field_name='info_biz', lookup_expr='icontains', )
    deal = django_filters.CharFilter(label='주요거래처', field_name='deal', lookup_expr='icontains', )
    possible_set = django_filters.CharFilter(label='개발가능제품분야', field_name='possible_set', lookup_expr='in', )
    history_set = django_filters.CharFilter(label='진행한제품들', field_name='history_set', lookup_expr='in', )
    #ordering = django_filters.CharFilter(label='순서', method='filter_ordering')

    class Meta:
        model = Partner
        fields = ['name', 'info_company', 'info_biz', 'deal', 'possible_set', 'history_set']
                  #'ordering', ]

  #  def filter_ordering(self, queryset, name, value):
  #      if value == 'review': # 리뷰 많은 순
  #          ids = list(LinkerReview.objects.values('profile'
  #                      ).annotate(count=Count('profile')).order_by('-count'
  #                      ).values_list('profile__linker__id', flat=True))
  #          linker_ids = list(queryset.values_list('id', flat=True))
  #          for id in linker_ids:
  #              if id not in ids:
  #                  ids.append(id)
  #          preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
  #          return queryset.filter(pk__in=ids).order_by(preserved)

  #      if value == 'score': # 평점 높은 순
  #          return queryset.order_by('-average_score')

  #      if value == 'solved_business': # 해결한 비즈니스
  #          ids = list(BusinessApplication.objects.all().completed(
  #                ).values('profile').annotate(count=Count('profile')).order_by('-count'
  #                ).values_list('profile__linker__id', flat=True))
  #          linker_ids = list(queryset.values_list('id', flat=True))
  #          for id in linker_ids:
  #              if id not in ids:
  #                  ids.append(id)
  #          preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
  #          return queryset.filter(pk__in=ids).order_by(preserved)

  #      if value == '-signup':
  #          return queryset.order_by('-profile__user__date_joined')

  #      if value == 'signup':
  #          return queryset.order_by('profile__user__date_joined')