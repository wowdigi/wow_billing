from .models import *
from .serializers import *
from rest_framework import viewsets ,views
from rest_framework.response import Response


# Create your views here.

class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = BillingMstSerializer
    queryset = BillingMst.objects.filter(is_active = True, is_deleted = False).order_by('-id')

class CountryView(views.APIView):
    def get(self, request):
        queryset = Country.objects.filter(is_deleted = False, is_active = True).order_by('name').values('id','name','symbol')
        return Response(queryset)