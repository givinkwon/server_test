from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.category.models import *
from apps.project.models import *
from api.project.serializers import * # 카테고리가 프로젝트를 가져오는 구조 / 상호 참조 주의하기

class SubclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subclass
        fields = ['maincategory','category','id','subclass', 'small_img']

class CategorySerializer(serializers.ModelSerializer):
    subclass_set = SubclassSerializer(many=True)
    class Meta:
        model = Category
        fields = ['maincategory', 'id','category', 'middle_img','subclass_set']

class MaincategorySerializer(serializers.ModelSerializer):
    category_set = CategorySerializer(many=True)
    class Meta:
        model = Maincategory
        fields = ['id', 'maincategory', 'big_img', 'category_set']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id','city', 'region']


class CitySerializer(serializers.ModelSerializer):
    region_set = RegionSerializer(many=True)
    class Meta:
        model = City
        fields = ['id', 'city', 'region_set']

class DevelopSerializer(serializers.ModelSerializer):
    select_set = SelectSerializer(many=True)
    class Meta:
        model = Develop
        fields = ['id','maincategory', 'category', 'coin', 'select_set']

class DevelopbigSerializer(serializers.ModelSerializer):
    develop_set = DevelopSerializer(many=True)
    class Meta:
        model = Developbig
        fields = ['id','maincategory', 'develop_set']