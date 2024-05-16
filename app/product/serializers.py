from rest_framework import serializers
from .models import Market


class MarketSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source='place.name', read_only=True)

    class Meta:
        model = Market
        fields = ('id', 'place_name')
