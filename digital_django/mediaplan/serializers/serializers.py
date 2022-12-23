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
class CountrySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = [
            "id",
            "code",
            "name",
        ]

class TargetCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetCountry
        fields = [
            "id",
            "strategy",
            "country",
            "code",
            "name",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            ]
        
    def create(self, validated_data):
        target_country, created = TargetCountry.objects.update_or_create(
            strategy=validated_data['strategy'],
            country=validated_data['country'],
            defaults={
                'code': validated_data['code'],
                'name': validated_data['name'],
                'budget': validated_data['budget'],
                'budget_allocated': validated_data['budget_allocated'],
                'auto_allocate': validated_data['auto_allocate'],
                })
        return target_country
        
class ChannelSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Channel
        fields = [
            "id",
            "code",
            "name",
        ]
class TargetChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetChannel
        fields = [
            "id",
            "target_country",
            "channel",
            "code",
            "name",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            ]

    def create(self, validated_data):
        print(f'validated_data: {validated_data}')
        target_channel, created = TargetChannel.objects.update_or_create(
            target_country=validated_data['target_country'],
            channel=validated_data['channel'],
            defaults={
                'code': validated_data['code'],
                'name': validated_data['name'],
                'budget': validated_data['budget'],
                'budget_allocated': validated_data['budget_allocated'],
                'auto_allocate': validated_data['auto_allocate'],
                })
        return target_channel

class TargetDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetDevice
        fields = [
            "id",
            "target_channel",
            "device",
            "code",
            "name",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            ]

    def create(self, validated_data):
        print(f'TargetDeviceSerializer: create: validated_data: {validated_data}')
        target_device, created = TargetDevice.objects.update_or_create(
            target_channel=validated_data['target_channel'],
            device=validated_data['device'],
            defaults={
                'code': validated_data['code'],
                'name': validated_data['name'],
                'budget': validated_data['budget'],
                'budget_allocated': validated_data['budget_allocated'],
                'auto_allocate': validated_data['auto_allocate'],
                })
        return target_device

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = [
            "id",
            "code",
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

