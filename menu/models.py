from django.db import models

class Product(models.Model):
    CATEGORIES = [
        ('MAIN', 'Main'),
        ('APETIZER', 'Apetizer'),
        ('DESSERT', 'Dessert'),
        ('DRINK', 'Drink'),
    ]
    name = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    has_stock = models.BooleanField(default=True)
    description = models.CharField(max_length=500, blank=True)