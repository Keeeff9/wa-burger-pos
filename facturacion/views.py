from django.shortcuts import render, redirect
from random import randint
from decimal import Decimal
from django.utils import timezone

from facturacion.models import Invoice, InvoiceDetail


def generate_invoice(request):

    # Usar request.session en lugar del caché
    cart = request.session.get("cart", {})

    print("CARRITO:", cart)  # Debug

    if not cart:
        return redirect("menu:menu_list")

    details = []
    for product_id, item in cart.items():
        subtotal = Decimal(str(item["price"])) * item["quantity"]
        details.append({
            "name": item["name"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
        })

    subtotal_total = sum(d["subtotal"] for d in details)

    tax = subtotal_total * Decimal("0.19")

    total = subtotal_total + tax

    invoice_number = f"INV-{timezone.now():%Y%m%d}-{randint(100,999)}"

    invoice = Invoice.objects.create(
        invoice_number=invoice_number,
        subtotal=subtotal_total,
        tax=tax,
        total=total,
        payment_status="PAID"
    )

    for product_id, item in cart.items():
        item_subtotal = Decimal(str(item["price"])) * item["quantity"]
        InvoiceDetail.objects.create(
            invoice=invoice,
            product_id=str(product_id),
            product_name=item["name"],
            quantity=item["quantity"],
            unit_price=item["price"],
            subtotal=item_subtotal
        )

    # Limpiar carrito
    request.session["cart"] = {}
    request.session.modified = True

    return render(
        request,
        "facturacion/invoice.html",
        {
            "invoice": invoice,
            "details": details
        }
    )