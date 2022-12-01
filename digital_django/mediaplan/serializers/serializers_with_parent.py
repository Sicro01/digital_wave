from rest_framework import serializers

from ..models import Phase, Strategy, Country

class PhaseSerializerWithParent(serializers.ModelSerializer):

    class Meta:
        model = Phase
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "slug",
            "get_absolute_url",
            "date_added",
            "plan"
        ]

class StrategySerializerWithParent(serializers.ModelSerializer):
        
    class Meta:
        model = Strategy
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "slug",
            "get_absolute_url",
             "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "phase",
        ]

class CountrySerializerWithParent(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    
    class Meta:
        model = Country
        fields = [
            "id",
            "code",
            "name",
            "strategies",
        ]
        extra_kwargs = {'strategies': {'required': False}}
    

