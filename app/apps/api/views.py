from rest_framework import mixins, viewsets

from .serializers import ConcernsSerializer
from app.apps.handling_concerns.models import Concerns

class ConcernViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Concerns.objects.all()
    serializer_class = ConcernsSerializer
