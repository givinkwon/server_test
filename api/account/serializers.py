from rest_framework import serializers
from apps.account.models import *
from apps.category.models import *
from apps.project.models import *
from api.project.serializers import *
from api.category.serializers import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'type', 'password', 'is_update','phone']

class PatchUserSerializer(serializers.ModelSerializer):
 #   user_data = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username', 'type','phone']
        #,'user_data']

 #   def get_user_data(self,obj):
 #       if type == 0:
 #           a = Client.objects.filter(user=obj.id)
 #           return ClientSerializer(a,many=True).data
 #       b= Partner.objects.filter(user=obj.id)
 #       return PartnerSerializer(b,many=True).data

class ClientSerializer(serializers.ModelSerializer):
    request_set = RequestSerializer(many=True)
    answer_set = AnswerSerializer(many=True)
    review_set = ReviewSerializer(many=True)
    class Meta:
        model = Client
        fields = ['user','id','request_set','answer_set','review_set']

class PartnerSerializer(serializers.ModelSerializer):
    avg_score = serializers.SerializerMethodField()
    product_possible = serializers.SerializerMethodField()
    product_history = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    answer_set = AnswerSerializer(many=True)
    review_set = ReviewSerializer(many=True)
    class Meta:
        model = Partner
        fields = ['user','id', 'name', 'logo', 'city', 'region', 'career', 'employee', 'revenue', 'info_company', 'info_biz','history', 'deal' ,'category', 'product_possible', 'product_history', 'coin','avg_score','answer_set','review_set','file']

    def get_avg_score(self,obj):
        a = Review.objects.filter(partner=obj.id).aggregate(Avg('price_score'))
        b = Review.objects.filter(partner=obj.id).aggregate(Avg('time_score'))
        c = Review.objects.filter(partner=obj.id).aggregate(Avg('talk_score'))
        d = Review.objects.filter(partner=obj.id).aggregate(Avg('expert_score'))
        e = Review.objects.filter(partner=obj.id).aggregate(Avg('result_score'))
        if not a['price_score__avg'] is None: # 리뷰가 있으면
            avg_score = (a['price_score__avg'] + b['time_score__avg'] + c['talk_score__avg'] + d['expert_score__avg'] + e['result_score__avg']) / 5
            obj.avg_score = avg_score
            obj.save()
            return avg_score
        return 0

    def get_product_possible(self, obj):
        a=obj.possible_set # many to many는 양쪽에 FK로 작용 > obj.possible_set이 데이터베이스 테이블(모델) 및 Queryset
        return SubclassSerializer(a,many=True).data

    def get_product_history(self, obj):
        a=obj.history_set # many to many는 양쪽에 FK로 작용 > obj.possible_set이 데이터베이스 테이블(모델) 및 Queryset
        return SubclassSerializer(a,many=True).data

    def get_category(self, obj):
        a=obj.category_middle # many to many는 양쪽에 FK로 작용 > obj.possible_set이 데이터베이스 테이블(모델) 및 Queryset
        return DevelopSerializer(a,many=True).data

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['partner','img_portfolio']

class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ['partner','img_structure']

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['partner','img_machine']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['partner','img_certification']

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['partner','img_process']
