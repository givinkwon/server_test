from rest_framework import serializers
from apps.project.models import *

#시간 관련 함수
from django.utils import timezone
from datetime import date

now = timezone.localtime()

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['active', 'time_out', 'created_at', 'id', 'client', 'project', 'product','category', 'price', 'day', 'content', 'name','request1','request2','request3','request4','request5','request6','request7','request8','file','created_at','apply_count', 'coin']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'request', 'content1', 'content2', 'content3', 'content4']

class SelectSerializer(serializers.ModelSerializer):
    content_set = ContentSerializer(many=True)
    class Meta:
        model = Select
        fields = ['id', 'category', 'content_set']

class CommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ['id', 'product', 'price', 'day', 'content','file']

class AnswerSerializer(serializers.ModelSerializer):
    writed_review = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['state', 'active','created_at', 'id', 'client','project', 'partner', 'price', 'day', 'expert', 'strategy', 'see_phone', 'see_review', 'down_chage','writed_review']

    def get_writed_review(self, obj):
        review_qs = Review.objects.filter(project=obj.project)
        if review_qs.exists():
            return True
        return False

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['client', 'project', 'partner', 'price_score', 'time_score', 'talk_score', 'expert_score', 'result_score', 'content', 'avg_score']


class ProjectSerializer(serializers.ModelSerializer):
    # 외래키 참조시 자동으로 모델이름_set 테이블이 만들어지며 모두 소문자로 변경
    request_set = RequestSerializer(many=True)
    answer_set = AnswerSerializer(many=True)
    review_set = ReviewSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'request_set', 'answer_set', 'review_set']
