from rest_framework import serializers

from ..models import Phase, Strategy, Country
from .serializers import StrategySerializer, CountrySerializer, TargetCountrySerializer

class PhaseSerializerWithParentChild(serializers.ModelSerializer):
    strategies = StrategySerializer(many=True)

    class Meta:
        model = Phase
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "slug",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            "plan",
            "strategies"
        ]

    def create(self, validated_data):
        print(f'Phase validated_data: {validated_data}')
        plan = validated_data.pop('plan')
        strategies = validated_data.pop('strategies')
        phase = Phase.objects.create(plan=plan, **validated_data)

        for strategy in strategies:
            Strategy.objects.create(phase=phase, **strategy)

        return phase

class StrategySerializerWithParentChild(serializers.ModelSerializer):
    targetcountries = TargetCountrySerializer(many=True)
        
    class Meta:
        model = Strategy
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "slug",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            "phase",
            "targetcountries",
        ]