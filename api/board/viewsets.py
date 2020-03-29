#from django.contrib.auth.models import Group
from apps.board.models import *
from rest_framework import viewsets
from .serializers import *

class NoticeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class MagazineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer
