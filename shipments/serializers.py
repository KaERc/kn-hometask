from rest_framework import serializers

from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ["id", "reference", "origin", "destination", "status", "eta"]

    def validate(self, attrs):
        # On PATCH only some fields arrive, so fall back to the stored values.
        origin = attrs.get("origin", getattr(self.instance, "origin", None))
        destination = attrs.get(
            "destination", getattr(self.instance, "destination", None)
        )
        if origin and destination and origin.casefold() == destination.casefold():
            raise serializers.ValidationError(
                {"destination": "Destination must differ from origin."}
            )
        return attrs
