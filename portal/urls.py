from django.urls import path , include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('billing', BillingViewSet, basename='billing')

urlpatterns = [
    path('', include(router.urls)),
    path('currency/', CountryView.as_view(), name='currency'),
  
]