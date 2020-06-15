from rest_framework import serializers
from apps.project.models import *


from django.utils import timezone
from datetime import date

now = timezone.localtime()

class RequestSerializer(serializers.ModelSerializer):
    count_answer = serializers.SerializerMethodField()
    class Meta:
        model = Request
        fields = ['count_answer','active', 'time_out', 'created_at', 'id', 'client', 'project', 'product','category', 'price', 'day', 'content', 'name','file','created_at','apply_count', 'coin','complete', 'add_meeting', 'examine']
        read_only_fields = ['project']

    def get_count_answer(self, obj):
        answer_qs = Answer.objects.filter(project=obj.id)
        if answer_qs.exists():
            return answer_qs.count()
        return 0

class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ['id', 'request', 'content1', 'content2', 'content3', 'content4']

class SelectSerializer(serializers.ModelSerializer):
    content_set = ContentSerializer(many=True)
    class Meta:
        model = Select
        fields = ['id', 'category', 'request', 'content_set']

class Select_saveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Select_save
        fields = ['id', 'category', 'request', 'question', 'answer']

class CommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ['id', 'product', 'price', 'day', 'content','file']
#-*- coding: cp949 -*-
class AnswerSerializer(serializers.ModelSerializer):
    writed_review = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['state', 'active','created_at', 'id', 'client','project', 'partner', 'category', 'people', 'price',  'strategy', 'period', 'day', 'all_price', 'expert', 'see_phone', 'see_review', 'down_chage','writed_review','file']

    def get_writed_review(self, obj):
        review_qs = Review.objects.filter(project=obj.project)
        if review_qs.exists():
            return True
        return False

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'client', 'project', 'partner', 'price_score', 'time_score', 'talk_score', 'expert_score', 'result_score', 'content_good', 'content_bad', 'avg_score']


class ProjectSerializer(serializers.ModelSerializer):

    request_set = RequestSerializer(many=True, read_only=True)
    answer_set = AnswerSerializer(many=True, read_only=True)
    review_set = ReviewSerializer(many=True, read_only=True)
    count_answer = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['count_answer','count_review','id', 'request_set', 'answer_set', 'review_set']
        read_only_fields = ['request_set', 'answer_set', 'review_set']

    def get_count_answer(self, obj):
        answer_qs = Answer.objects.filter(project=obj.id)
        if answer_qs.exists():
            return answer_qs.count()
        return 0

    def get_count_review(self, obj):
        review_qs = Review.objects.filter(project=obj.id)
        if review_qs.exists():
            return review_qs.count()
        return 0