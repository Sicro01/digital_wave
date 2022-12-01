from rest_framework import serializers

from ..models import Phase, Strategy, Country, Channel, Device, Ad, Creative, TargetCountry, TargetChannel, TargetDevice, TargetAd

class PhaseSerializer(serializers.ModelSerializer):

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
             "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
        ]

class StrategySerializer(serializers.ModelSerializer):

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
            "date_modified",
        ]
    
class TargetCountrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TargetCountry
        fields = [
            "strategy",
            "country",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            ]

class CountrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = [
            "id",
            "code",
            "name",
        ]

class ChannelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Channel
        fields = [
            "id",
            "code",
            "name",
        ]

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
        ]

class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
        ]

class CreativeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Creative
        fields = [
            "id",
            "name",
        ]

