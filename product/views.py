from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Discount
from .serializers import ProductSerializer


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = []

        for product in products:
            # Get global and product-specific discounts
            discounts = Discount.objects.filter(global_discount=True) | Discount.objects.filter(product=product)

            # Apply the best discount
            original_price = product.price
            best_discount = None
            final_price = original_price

            for discount in discounts:
                if discount.discount_type == Discount.PERCENTAGE:
                    discounted_price = original_price * (1 - discount.value / 100)
                elif discount.discount_type == Discount.FIXED:
                    discounted_price = original_price - discount.value

                if discounted_price < final_price:
                    final_price = discounted_price
                    best_discount = discount

            # Append the final data
            data.append({
                'product': ProductSerializer(product).data,
                'original_price': original_price,
                'final_price': final_price,
                'applied_discount': best_discount.name if best_discount else None
            })

        return Response(data)
