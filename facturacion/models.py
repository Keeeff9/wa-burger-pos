from django.db import models
from django.utils import timezone


class Invoice(models.Model):

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        default="PAID"
    )

def __str__(self):
        return self.invoice_number

class InvoiceDetail(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE
    )

    product_id = models.CharField(max_length=50)

    product_name = models.CharField(max_length=100)

    quantity = models.IntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )