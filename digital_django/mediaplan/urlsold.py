from django.urls import path
from mediaplan import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("plans", views.PlanViewSet, basename="plans")
# urlpatterns = router.urls

# plan_list = views.PlanViewSet.as_view({"get": "list"})
appname = "mediaplan"

urlpatterns = [
    path("plans/", views.PlanViewSet.as_view()),
    path("addplan/", views.addplan),
]
