from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from auth_app.serializers import UserProfileSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_with_profile(request):
    user_data = {
        "username": request.data.get('username'),
        "email": request.data.get('email'),
        "password": request.data.get('password'),
    }

    profile_data = {
        "phone": request.data.get('phone'),
        "address": request.data.get('address'),
        "adharcard": request.data.get('adharcard'),
        "is_farmer": request.data.get('is_farmer', False),
        "acre_of_land": request.data.get('acre_of_land', None),
        "kisan_card": request.data.get('kisan_card', None),
        "is_buyer": request.data.get('is_buyer', False),
        "gst": request.data.get('gst', None)
    }

    # Check for missing fields in user data
    missing_user_fields = [key for key,
                           value in user_data.items() if not value]
    if missing_user_fields:
        return Response({
            "status_code": 6001,
            "message": f"Missing required user fields: {', '.join(missing_user_fields)}"
        }, status=400)

    # Check for missing fields in profile data
    missing_profile_fields = []
    # If the user is a farmer, check for farm-specific fields
    if profile_data['is_farmer']:
        if not profile_data['acre_of_land']:
            missing_profile_fields.append('acre_of_land')
        if not profile_data['kisan_card']:
            missing_profile_fields.append('kisan_card')
    # If the user is a buyer, check for buyer-specific fields
    if profile_data['is_buyer']:
        if not profile_data['gst']:
            missing_profile_fields.append('gst')

    # Common profile fields
    common_profile_fields = ['phone', 'address', 'adharcard']
    missing_profile_fields += [
        key for key in common_profile_fields if not profile_data[key]]

    if missing_profile_fields:
        return Response({
            "status_code": 6001,
            "message": f"Missing required profile fields: {', '.join(missing_profile_fields)}"
        }, status=400)

    # Serializers
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        profile_serializer = UserProfileSerializer(
            data=profile_data, context={'user_data': user_data})

        # Validate and save user and profile data
        if user_serializer.is_valid() and profile_serializer.is_valid():
            profile_serializer.save()
            return Response({"status_code": 6000, "message": "User created successfully"}, status=201)
        else:
            return Response({
                "status_code": 6001,
                "message": "Invalid data",
                "user_errors": user_serializer.errors,
                "profile_errors": profile_serializer.errors
            }, status=400)
    else:
        # User validation errors
        return Response({
            "status_code": 6001,
            "message": "User already exist",
            "errors": user_serializer.errors
        }, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({
            "status_code": 6001,
            "message": "Please provide both username and password"
        }, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "status_code": 6000,
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=200)
    else:
        return Response({
            "status_code": 6001,
            "message": "Invalid username or password"
        }, status=400)
