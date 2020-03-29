from apps.payment.models import *
from rest_framework import viewsets
from .serializers import *

class PaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Paylist.objects.all()
    serializer_class = PaylistSerializer