from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'phone', 'address',
            'adharcard', 'is_farmer', 'acre_of_land', 'kisan_card',
            'is_buyer', 'gst'
        ]

    def create(self, validated_data):
        user_data = self.context['user_data']
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
