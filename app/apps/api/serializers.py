from rest_framework import serializers

from app.apps.handling_concerns.models import Concerns

class ConcernsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concerns
        fields = '__all__'