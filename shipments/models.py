from django.db import models


class Shipment(models.Model):
    # ponytail: no created_at/updated_at and no history of status changes, and with
    # no authentication there is no author to record either; add timestamps and
    # django-simple-history when users or claims handling arrive.
    class Status(models.TextChoices):
        BOOKED = "booked", "Booked"
        IN_TRANSIT = "in_transit", "In transit"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    reference = models.CharField(max_length=32, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.BOOKED
    )
    eta = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
