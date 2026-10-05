from rest_framework import filters, viewsets

from .models import Shipment
from .serializers import ShipmentSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    # ponytail: unpaginated, so every list call returns the whole table; switch on
    # DRF's PageNumberPagination when the list outgrows a screen or two.
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [filters.SearchFilter]
    # ponytail: SQLite matches case-insensitively for ASCII only ("Ülemiste" is
    # not found by "ülemiste"); Postgres, or Elasticsearch at volume, fixes it.
    search_fields = ["reference", "origin", "destination"]
