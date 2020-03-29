#from django.contrib.auth.models import Group
from apps.category.models import *
from rest_framework import viewsets
from .serializers import *

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class MaincategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Maincategory.objects.all()
    serializer_class = MaincategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    #filterset_fields = []
    search_fields = ['maincategory', 'category__category', 'subclass__subclass'] # 자동으로 FK 테이블 관련 데이터를 가져올 수 있음

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubclassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Subclass.objects.all()
    serializer_class = SubclassSerializer

class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer

class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DevelopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Develop.objects.all()
    serializer_class = DevelopSerializer

class DevelopbigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Developbig.objects.all()
    serializer_class = DevelopbigSerializer
