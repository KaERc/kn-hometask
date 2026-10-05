from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shipments.views import ShipmentViewSet

router = DefaultRouter()
router.register("shipments", ShipmentViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
