from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from auth_app.models import UserProfile
from rest_framework import status
from django.db import IntegrityError
from .models import Auction, Bid, Wallet, Escrow
from decimal import Decimal

from .serializers import FarmerProfileSerializer, BuyerProfileSerializer, AuctionSerializer, BidSerializer, WalletSerializer

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
def create_auction(request):
    # Get the authenticated user
    buyer = request.user

    data = request.data.copy()

    # Assign the buyer as the authenticated user object, not just the ID
    data['buyer'] = buyer.id

    # Serialize the incoming data
    serializer = AuctionSerializer(data=data)

    try:
        # Check if the data is valid and save it if so
        if serializer.is_valid():
            serializer.save(buyer=buyer)  # Pass the buyer object explicitly
            return Response({
                "status_code": 6000,
                "message": "Auction created successfully",
                "auction": serializer.data
            }, status=status.HTTP_201_CREATED)

        # If the data is not valid, return validation errors
        error_messages = []
        for field, errors in serializer.errors.items():
            error_messages.append(f"{field}: {', '.join(errors)}")

        return Response({
            "status_code": 6001,
            "message": "Auction creation failed. Please fix the following errors:",
            "errors": error_messages
        }, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        # Handle the IntegrityError (like NOT NULL constraint)
        return Response({
            "status_code": 6002,
            "message": "Auction creation failed due to a database integrity error.",
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_auctions(request):
    auctions = Auction.objects.all()  # Retrieve all auctions

    if not auctions.exists():  # Check if there are any auctions
        return Response({
            "status_code": 6002,
            "message": "No auctions found.",
            "auctions": []
        }, status=404)

    serializer = AuctionSerializer(auctions, many=True)
    return Response({
        "status_code": 6000,
        "message": "List of auctions retrieved successfully",
        "auctions": serializer.data
    }, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_bid(request):
    auction_id = request.data.get('auction_id')
    bid_amount = request.data.get('bid_amount')
    bid_quantity = request.data.get('bid_quantity')

    if not auction_id or not bid_amount or not bid_quantity:
        return Response({"message": "auction_id,bid_quantityand bid_amount are required"}, status=400)

    auction = Auction.objects.filter(id=auction_id).first()
    if not auction:
        return Response({"message": "Auction not found"}, status=404)

    bid = Bid.objects.create(
        auction=auction,
        bidder_name=request.user.username,
        bid_amount=bid_amount,
        bid_quantity=bid_quantity
    )

    # Optionally, send this bid to Firebase as well
    # Add Firebase logic here if necessary

    return Response({"message": "Bid submitted successfully", "bid": BidSerializer(bid).data}, status=201)


@api_view(['POST'])
def accept_bid(request):
    buyer_id = request.data.get('buyer_id')
    bid_id = request.data.get('bid_id')

    try:
        # Fetch the bid based on the bid_id
        bid = Bid.objects.get(id=bid_id)

        # Fetch the buyer's wallet
        buyer_wallet = Wallet.objects.get(user_id=buyer_id)

        # Calculate the escrow amount (20% of the bid amount)
        escrow_amount = (bid.bid_amount * bid.bid_quantity) * Decimal('0.20')

        # Check if the buyer has enough balance
        if buyer_wallet.balance >= escrow_amount:
            # Deduct the amount from buyer's wallet
            buyer_wallet.balance -= escrow_amount
            buyer_wallet.save()  # Save changes to the database

            # Deposit the amount into escrow
            Escrow.objects.create(bid=bid, amount=escrow_amount)

            return Response({
                'status': 'success',
                'message': f'Bid accepted. {escrow_amount} deposited in escrow.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failure',
                'message': 'Insufficient balance.'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Bid.DoesNotExist:
        return Response({
            'status': 'failure',
            'message': 'Bid not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Wallet.DoesNotExist:
        return Response({
            'status': 'failure',
            'message': 'Wallet not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'failure',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet(request):
    wallet = Wallet.objects.all()  # Retrieve all auctions

    if not wallet.exists():  # Check if there are any auctions
        return Response({
            "status_code": 6002,
            "message": "wallet is empty",
            "auctions": []
        }, status=404)

    serializer = WalletSerializer(wallet, many=True)
    return Response({
        "status_code": 6000,
        "message": "wallet balance retrieved successfully",
        "data": serializer.data
    }, status=200)
