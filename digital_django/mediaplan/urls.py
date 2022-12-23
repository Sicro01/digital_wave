from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mediaplan import views

app_name='digital_wave_api'

router = DefaultRouter()
router.register('targetcountries', views.TargetCountryViewSet, basename='targetcountries')
router.register('targetchannels', views.TargetChannelViewSet, basename='targetchannels')
router.register('targetdevices', views.TargetDeviceViewSet, basename='targetdevices')

urlpatterns = [
    path('plans/', views.PlanListCreate.as_view(), name='planlist'),
    path('plan/<int:pk>/', views.PlanDetail.as_view(), name='plandetail'),

    path('phases/', views.PhaseListCreate.as_view(), name='phaselist'),
    path('phase/<int:pk>/', views.PhaseDetail.as_view(), name='phasedetail'),

    path('strategies/', views.StrategyListCreate.as_view(), name='strategylist'),
    path('strategy/<int:pk>/', views.StrategyDetail.as_view(), name='strategydetail'),

    path('countries/', views.CountryListCreate.as_view(), name='country'),
    path('country/<int:pk>/', views.CountryDetail.as_view(), name='countrydetail'),

    path('channels/', views.ChannelListCreate.as_view(), name='channellist'),
    path('channel/<int:pk>/', views.ChannelDetail.as_view(), name='channeldetail'),

    path('devices/', views.DeviceListCreate.as_view(), name='devicelist'),
    path('device/<int:pk>/', views.DeviceDetail.as_view(), name='devicedetail'),

    path('ads/', views.AdListCreate.as_view(), name='adlist'),
    path('ad/<int:pk>/', views.AdDetail.as_view(), name='addetail'),

    path('creatives/', views.CreativeListCreate.as_view(), name='creativelist'),
    path('creative/<int:pk>/', views.CreativeDetail.as_view(), name='creativedetail'),
]

urlpatterns += router.urls
