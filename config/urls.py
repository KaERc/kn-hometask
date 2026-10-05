from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shipments.views import ShipmentViewSet

router = DefaultRouter()
router.register("shipments", ShipmentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
