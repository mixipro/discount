from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)  # SKU is unique
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Discount(models.Model):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'

    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
    ]

    name = models.CharField(max_length=255)
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default=PERCENTAGE,
    )
    value = models.FloatField(validators=[MinValueValidator(0.0)])
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='discounts', null=True, blank=True
    )
    global_discount = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_discount_type_display()} - {self.value})"