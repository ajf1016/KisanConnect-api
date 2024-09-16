from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import ChatRoom
from auth_app.models import UserProfile
from .serializers import FarmerProfileSerializer, BuyerProfileSerializer, ChatRoomSerializer

# API to search farmers based on location, crops, and rating


@api_view(['GET'])
@permission_classes([AllowAny])
def search_farmers(request):
    crops = request.query_params.get('crops', None)
    min_rating = request.query_params.get('min_rating', 0.0)

    # Create a Q object for filtering farmers
    filters = Q(is_farmer=True)

    if crops:
        # Search for farmers growing the specified crops
        filters &= Q(crops__icontains=crops)
    if min_rating:
        filters &= Q(rating__gte=min_rating)  # Filter by rating

    farmers = UserProfile.objects.filter(filters)

    if farmers.exists():
        serializer = FarmerProfileSerializer(farmers, many=True)
        return Response({
            "status_code": 6000,
            "message": "Farmers found",
            "farmers": serializer.data
        }, status=200)
    else:
        return Response({
            "status_code": 6001,
            "message": "No farmers found matching the criteria"
        }, status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_buyers(request):
    organization = request.query_params.get('organization', None)
    min_rating = request.query_params.get('min_rating', 0.0)

    # Create a Q object for filtering buyers
    filters = Q(is_buyer=True)

    if organization:
        # Filter by organization
        filters &= Q(organization__iexact=organization)
    if min_rating:
        filters &= Q(rating__gte=min_rating)  # Filter by rating

    buyers = UserProfile.objects.filter(filters)

    if buyers.exists():
        serializer = BuyerProfileSerializer(buyers, many=True)
        return Response({
            "status_code": 6000,
            "message": "Buyers found",
            "buyers": serializer.data
        }, status=200)
    else:
        return Response({
            "status_code": 6001,
            "message": "No buyers found matching the criteria"
        }, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_chat(request):
    buyer_id = request.data.get('buyer_id')
    farmer_id = request.data.get('farmer_id')

    if not buyer_id or not farmer_id:
        return Response({
            "status_code": 6001,
            "message": "Both buyer_id and farmer_id are required"
        }, status=400)

    try:
        chat_room, created = ChatRoom.objects.get_or_create(
            buyer_id=buyer_id, farmer_id=farmer_id)

        if created:
            return Response({
                "status_code": 6000,
                "message": "Chat room created successfully",
                "chat_room": ChatRoomSerializer(chat_room).data
            }, status=201)
        else:
            return Response({
                "status_code": 6000,
                "message": "Chat room already exists",
                "chat_room": ChatRoomSerializer(chat_room).data
            }, status=200)

    except Exception as e:
        return Response({
            "status_code": 6001,
            "message": str(e)
        }, status=500)
