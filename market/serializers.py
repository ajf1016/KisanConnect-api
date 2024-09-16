from .models import ChatRoom
from auth_app.models import UserProfile
from rest_framework import serializers


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


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'buyer', 'farmer', 'created_at']
