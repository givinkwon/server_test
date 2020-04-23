#from django.contrib.auth.models import Group
from apps.board.models import *
from rest_framework import viewsets
from .serializers import *
#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.account.filters import *

class NoticeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_top']

class MagazineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_top']