from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .serializers.serializers import    (PhaseSerializer, StrategySerializer, CountrySerializer, ChannelSerializer, DeviceSerializer,
                                        AdSerializer, CreativeSerializer, TargetCountrySerializer, TargetChannelSerializer, TargetDeviceSerializer)
from .serializers.serializers_with_child import PlanSerializerWithChild
from .serializers.serializers_with_parent_child import PhaseSerializerWithParentChild, StrategySerializerWithParentChild
from .serializers.serializers_with_parent import StrategySerializerWithParent, CountrySerializerWithParent

from .models import Plan, Phase, Strategy, Country, Channel, Device, Ad, Creative, TargetCountry, TargetChannel, TargetDevice

class PlanListCreate(ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializerWithChild

class PlanDetail(RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializerWithChild

class PhaseListCreate(ListCreateAPIView):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializerWithParentChild

class PhaseDetail(RetrieveUpdateDestroyAPIView):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer

class StrategyListCreate(ListCreateAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializerWithParent

class StrategyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

class TargetCountryViewSet(ModelViewSet):
    queryset = TargetCountry.objects.all()
    serializer_class = TargetCountrySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        strategy = self.request.query_params.get('strategy')
        if strategy is not None:
            queryset = queryset.filter(strategy=strategy)
        return queryset
        
    @action(methods=["DELETE"], detail=False)
    def delete(self, request, *args, **kwargs):
        strategy = self.request.query_params.get('strategy')
        target_country = self.request.query_params.getlist('target_country')
        countries_to_delete = TargetCountry.objects.filter(strategy=strategy, country__in=target_country)
        num_target_countries = len(countries_to_delete)
        countries_to_delete.delete()
        return Response({"status": f'{num_target_countries} Target Countries Deleted'})

class CountryListCreate(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializerWithParent

class TargetChannelViewSet(ModelViewSet):
    queryset = TargetChannel.objects.all()
    serializer_class = TargetChannelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        target_country_id = self.request.query_params.get('target_country_id')
        if target_country_id is not None:
            queryset = queryset.filter(target_country=target_country_id)
        return queryset
        
    @action(methods=["DELETE"], detail=False)
    def delete(self, request, *args, **kwargs):
        channel = self.request.query_params.get('target_channel_id')
        target_country = self.request.query_params.get('target_country_id')
        target_channels = TargetChannel.objects.filter(channel=channel, target_country=target_country)
        num_target_channels = len(target_channels)
        target_channels.delete()
        return Response({"status": f'{num_target_channels} Target Channels Deleted'})

class TargetDeviceViewSet(ModelViewSet):
    queryset = TargetDevice.objects.all()
    serializer_class = TargetDeviceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        target_channel_id = self.request.query_params.get('target_channel_id')
        if target_channel_id is not None:
            queryset = queryset.filter(target_channel=target_channel_id)
        return queryset
        
    @action(methods=["DELETE"], detail=False)
    def delete(self, request, *args, **kwargs):
        device = self.request.query_params.get('target_device_id')
        print(f'device: {device}')
        target_channel = self.request.query_params.get('target_channel_id')
        print(f'target_channel: {target_channel}')
        target_devices = TargetDevice.objects.filter(device=device, target_channel=target_channel)
        num_target_devices = len(target_devices)
        target_devices.delete()
        return Response({"status": f'{num_target_devices} Target Devices Deleted'})

class ChannelListCreate(ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class ChannelDetail(RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class DeviceListCreate(ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class AdListCreate(ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

class AdDetail(RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

class CreativeListCreate(ListCreateAPIView):
    queryset = Creative.objects.all()
    serializer_class = CreativeSerializer

class CreativeDetail(RetrieveUpdateDestroyAPIView):
    queryset = Creative.objects.all()
    serializer_class = CreativeSerializer












# class PlanViewSet(ModelViewSet):
#     # permission_classes = [IsAuthenticated]
#     queryset = Plan.objects.all()
#     serializer_class = PlanSerializer
#     http_method_names = ['get', 'post', 'put', 'delete']

# class PlanDetail(APIView):
#     def get_object(self, plan_slug):
#         try:
#             return Plan.objects.get(slug=plan_slug)
#         except Plan.DoesNotExist:
#             raise Http404

#     def get(self, request, plan_slug, format=None):
#         plan = self.get_object(plan_slug)
#         serializer = PlanSerializer(plan)
#         return Response(serializer.data)

# class PhaseViewSet(ModelViewSet):
#     queryset = Phase.objects.all()
#     serializer_class = PhaseSerializer
#     http_method_names = ['get', 'post', 'put', 'delete']

