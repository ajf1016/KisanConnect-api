# auction/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Bid
from .serializers import ProductSerializer, BidSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET'])
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
def place_bid(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.end_time <= timezone.now():
        return Response({'error': 'The auction has ended.'}, status=status.HTTP_400_BAD_REQUEST)

    amount = request.data.get('amount', None)
    if not amount:
        return Response({'error': 'Bid amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if product.current_bid and product.current_bid.amount >= int(amount):
        return Response({'error': 'Bid must be higher than the current bid.'}, status=status.HTTP_400_BAD_REQUEST)

    # Place the bid
    bid = Bid.objects.create(user=request.user, product=product, amount=amount)
    product.current_bid = bid
    product.save()

    serializer = BidSerializer(bid)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
