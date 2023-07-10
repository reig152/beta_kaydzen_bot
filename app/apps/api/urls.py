from django.urls import path, include
from rest_framework import routers

from .views import ConcernViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'concerns_api',
                ConcernViewSet,
                basename='concerns_api')

urlpatterns = [
    path('v1/', include(router.urls)),
]
