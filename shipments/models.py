from django.db import models


class Shipment(models.Model):
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
