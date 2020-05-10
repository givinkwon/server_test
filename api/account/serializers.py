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
    client_class = serializers.SerializerMethodField()
    request_set = RequestSerializer(many=True)
    answer_set = AnswerSerializer(many=True)
    review_set = ReviewSerializer(many=True)
    user = PatchUserSerializer()
    class Meta:
        model = Client
        fields = ['user','id','request_set','answer_set','review_set', 'client_class']

    def get_client_class(self,obj):
        now = timezone.now()
        a = Clientclass.objects.filter(client = obj.id, end_time__gt = now)
        if a.exists():
            return True
        return False

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id','partner','img_portfolio','is_main']

class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ['id','partner','img_structure','is_main']

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id','partner','img_machine','is_main']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id','partner','img_certification','is_main']

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['id','partner','img_process','is_main']

class PartnerSerializer(serializers.ModelSerializer):
    avg_price_score = serializers.SerializerMethodField()
    avg_time_score = serializers.SerializerMethodField()
    avg_talk_score = serializers.SerializerMethodField()
    avg_expert_score = serializers.SerializerMethodField()
    avg_result_score = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    product_possible = serializers.SerializerMethodField()
    product_history = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    meeting_count = serializers.SerializerMethodField()
    meeting = serializers.SerializerMethodField()
    user = PatchUserSerializer()
    answer_set = AnswerSerializer(many=True)
    review_set = ReviewSerializer(many=True)
    portfolio_set = PortfolioSerializer(many=True)
    structure_set = StructureSerializer(many=True)
    machine_set = MachineSerializer(many=True)
    certification_set = CertificationSerializer(many=True)
    process_set = ProcessSerializer(many=True)
    class Meta:
        model = Partner
        fields = ['user','id', 'name', 'logo','city', 'region', 'career', 'employee', 'revenue', 'info_company', 'info_biz', 'deal' ,'category_middle','category', 'possible_set','product_possible', 'history_set', 'product_history', 'coin','avg_score',
                  'avg_price_score','avg_time_score','avg_talk_score','avg_expert_score','avg_result_score', 'answer_set','review_set','file','portfolio_set','structure_set', 'machine_set', 'certification_set', 'process_set', 'success', 'fail', 'meeting_count', 'meeting']

    def get_avg_price_score(self,obj):
        a = Review.objects.filter(partner=obj.id).aggregate(Avg('price_score'))
        if not a['price_score__avg'] is None: # 리뷰가 있으면
            return a
        return 0

    def get_avg_time_score(self,obj):
        b = Review.objects.filter(partner=obj.id).aggregate(Avg('time_score'))
        if not b['time_score__avg'] is None: # 리뷰가 있으면
            return b
        return 0

    def get_avg_talk_score(self,obj):
        c = Review.objects.filter(partner=obj.id).aggregate(Avg('talk_score'))
        if not c['talk_score__avg'] is None: # 리뷰가 있으면
            return c
        return 0

    def get_avg_expert_score(self,obj):
        d = Review.objects.filter(partner=obj.id).aggregate(Avg('expert_score'))
        if not d['expert_score__avg'] is None: # 리뷰가 있으면
            return d
        return 0

    def get_avg_result_score(self,obj):
        e = Review.objects.filter(partner=obj.id).aggregate(Avg('result_score'))
        if not e['result_score__avg'] is None: # 리뷰가 있으면
            return e
        return 0

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

    def get_meeting_count(self, obj):
        meeting_count=0
        answer_qs = Answer.objects.filter(partner=obj.id, state=1)
        if answer_qs.exists():
           return len(answer_qs)
        return 0
    #    print(list(answer_state))
    #    for state in list(answer_state):
    #        if state == '1':
    #            meeting_count += 1
    #    return meeting_count

    def get_meeting(self, obj):
        meeting_count = (obj.success + obj.fail)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        if meeting_count == 0:
            if not obj.success == 0:  # 미팅 성공이 1회 이상인 경우
                obj.meeting = 100
            else:  # 미팅 성공이 0회인 경우
                obj.meeting = 0
        else:
            obj.meeting = obj.success / meeting_count

        meeting_percent = obj.meeting
        print(obj.meeting)
        obj.save()

        return meeting_percent