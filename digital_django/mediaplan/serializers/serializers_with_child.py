from rest_framework import serializers

from ..models import Plan, Phase, Strategy, Country, Channel, Device, Ad, Creative
from .serializers import    (PhaseSerializer, StrategySerializer, CountrySerializer, ChannelSerializer, DeviceSerializer,
                            AdSerializer, CreativeSerializer, TargetCountrySerializer)
# from .serializers_with_child import PhaseSerializerWithChild

# class StrategySerializerWithChild(serializers.ModelSerializer):
#     targetcountries = TargetCountrySerializer(many=True)
    
#     class Meta:
#         model = Strategy
#         fields = [
#              "id",
#             "name",
#             "description",
#             "start_date",
#             "end_date",
#             "slug",
#             "get_absolute_url",
#             "budget",
#             "budget_allocated",
#             "auto_allocate",
#             "date_added",
#             "date_modified",
#         ]
        
#     def update(self, instance, validated_data):
#         # Update and save Strategy
#         target_country_data = validated_data.pop('targetcountries')
#         strategyObj = super().update(instance, validated_data)
#         strategyObj.save()


        # Get list of coutries to replac existing list and update this Strategy's countries
        # for target_country in target_country_data:
       
        
    
        # return strategyObj

class PhaseSerializerWithChild(serializers.ModelSerializer):
    strategies = StrategySerializer(many=True)
    # id = serializers.IntegerField(required=False)

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
            "strategies",
        ]

#     def create(self, validated_data):
#         print(f'Strategy validated_data: {validated_data}')
#         strategies = validated_data.pop('strategies')
#         phase = Phase.objects.create(**validated_data)

#         for strategy in strategies:
#             Strategy.objects.create(phase=strategy, **phase)

        # return phase

class PlanSerializerWithChild(serializers.ModelSerializer):
    phases = PhaseSerializerWithChild(many=True)

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "description",
            "slug",
            "get_absolute_url",
            "budget",
            "budget_allocated",
            "auto_allocate",
            "date_added",
            "date_modified",
            "phases",
        ]

    def create(self, validated_data):
        phase_data = validated_data.pop('phases')
        planObj = Plan.objects.create(**validated_data)

        for phase in phase_data:
            strategy_data = phase.pop('strategies')
            phaseObj = Phase.objects.create(plan=planObj, **phase)
            for strategy in strategy_data:
                strategyObj = Strategy.objects.create(phase=phaseObj, **strategy)
        return planObj

    def update(self, instance, validated_data):
        validated_phase_data = validated_data.pop('phases')
        planObj = super().update(instance, validated_data)
        planObj.save()
        return planObj

        # for phase in phase_data:
        #     strategy_data = phase.pop('strategies')
        #     phaseObj = Phase.objects.create(plan=planObj, **phase)
        #     for strategy in strategy_data:
        #         strategyObj = Strategy.objects.create(phase=phaseObj, **strategy)

        # for phase in validated_phase_data:
        #     check_phase_id = phase.get('id', None)
        #     if check_phase_id:
        #         existing_phase_item = Phase.objects.get(id=check_phase_id)
        #         existing_phase_item.name = phase.get('name', existing_phase_item.name)
        #         existing_phase_item.description = phase.get('description', existing_phase_item.description)
        #         existing_phase_item.start_date = phase.get('start_date', existing_phase_item.start_date)
        #         existing_phase_item.end_date = phase.get('end_date', existing_phase_item.end_date)
        #         existing_phase_item.save()
        #     else:
        #         Phase.objects.create(plan=instance, **phase)
        

class CountrySerializerWithChild(serializers.ModelSerializer):
    channels = ChannelSerializer()

    class Meta:
        model = Country
        fields = [
            "id",
            "code",
            "name",
            "channels",
        ]

class ChannelSerializerWithChild(serializers.ModelSerializer):
    devices = DeviceSerializer()

    class Meta:
        model = Channel
        fields = [
            "id",
            "name",
            "devices",
        ]

class DeviceSerializerWithChild(serializers.ModelSerializer):
    ads = AdSerializer()

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "ads",
        ]

class AdSerializerWithChild(serializers.ModelSerializer):
    creatives = CreativeSerializer()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "creatives",
        ]