from django.urls import path
from .views import (
    SupportTicketViewSet, 
    StatisticsViewSet, 
    StationViewSet,
    test_mongodb
)

urlpatterns = [
    path('support/', SupportTicketViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='support'),
    path('statistics/', StatisticsViewSet.as_view({
        'get': 'list'
    }), name='statistics'),
    path('stations/', StationViewSet.as_view({
        'get': 'list'
    }), name='stations'),
    path('test-mongodb/', test_mongodb, name='test-mongodb'),
]