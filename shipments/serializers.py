from rest_framework import serializers

from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ["id", "reference", "origin", "destination", "status", "eta"]

    def validate_reference(self, value):
        # unique=True compares exactly, so "kn-0001" would pass next to "KN-0001".
        # ponytail: two simultaneous requests can still pass this check together;
        # a unique constraint on Lower("reference") would close that gap.
        others = Shipment.objects.exclude(pk=getattr(self.instance, "pk", None))
        if others.filter(reference__iexact=value).exists():
            raise serializers.ValidationError(
                "A shipment with this reference already exists."
            )
        return value

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
