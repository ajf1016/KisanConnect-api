# auction/serializers.py
from rest_framework import serializers
from .models import Product, Bid


class BidSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ['user', 'product', 'amount', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    current_bid = BidSerializer(read_only=True)
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'current_bid', 'end_time', 'bids']
