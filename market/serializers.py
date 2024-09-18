from auth_app.models import UserProfile
from rest_framework import serializers
from .models import Auction, Bid, Wallet


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'crops', 'rating']


class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user',           # Link to the User model (username, email)
            'phone',          # Contact information
            'organization',   # Name of the organization (if applicable)
            'rating',         # Buyer rating (if applicable)
            'gst',            # GST number (for buyers)
            'is_buyer',       # To indicate if the user is a buyer
        ]


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'user',           # Link to the User model (username, email)
            'balance',          # Contact information
        ]


class AuctionSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()
    buyer_id = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'buyer_name', 'buyer_id', 'crop_name', 'variety_of_crop',
                  'quantity', 'price', 'is_completed', 'created_at']
        read_only_fields = ['buyer', 'created_at']

    def get_buyer_name(self, obj):
        return obj.buyer.username

    def get_buyer_id(self, obj):
        return obj.buyer.id


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder_name',
                  'bid_amount', 'bid_quantity']
        read_only_fields = ['id', 'created_at']  # Make these fields read-only

    def create(self, validated_data):
        # You can add custom logic here if needed before saving
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # You can add custom logic here if needed before updating
        return super().update(instance, validated_data)
