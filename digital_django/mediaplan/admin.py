from django.contrib import admin
from .models import Plan, Phase, Strategy, Country, Channel, Device, Ad, Creative, TargetCountry, TargetChannel, TargetDevice, TargetAd

admin.site.register(Plan)
admin.site.register(Phase)
admin.site.register(Strategy)
admin.site.register(Country)
admin.site.register(Channel)
admin.site.register(Device)
admin.site.register(Ad)
admin.site.register(Creative)
admin.site.register(TargetCountry)
admin.site.register(TargetChannel)
admin.site.register(TargetDevice)
admin.site.register(TargetAd)
