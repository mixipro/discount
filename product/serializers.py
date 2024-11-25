from rest_framework import serializers
from .models import Product, Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'name', 'discount_type', 'value', 'product', 'global_discount']


class ProductSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'price', 'discounts']
