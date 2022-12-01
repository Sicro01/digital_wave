from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .serializers.serializers import    (PhaseSerializer, StrategySerializer, CountrySerializer, ChannelSerializer, DeviceSerializer,
                                        AdSerializer, CreativeSerializer)
from .serializers.serializers_with_child import PlanSerializerWithChild, StrategySerializerWithChild
from .serializers.serializers_with_parent_child import PhaseSerializerWithParentChild, StrategySerializerWithParentChild
from .serializers.serializers_with_parent import StrategySerializerWithParent, CountrySerializerWithParent

from .models import Plan, Phase, Strategy, Country, Channel, Device, Ad, Creative

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

class CountryListCreate(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializerWithParent

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

