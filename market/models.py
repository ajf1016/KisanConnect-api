from django.db import models
from auth_app.models import UserProfile  # Reuse the UserProfile
from django.utils import timezone
from django.contrib.auth.models import User


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    # List of crops as a string, consider using a many-to-many field for more complex relationships
    crops = models.CharField(max_length=200)
    rating = models.FloatField(default=0.0)


class FarmerListing(models.Model):
    farmer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="farmer_listings")
    crop_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.FloatField(help_text="Quantity in kg or tons")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.crop_name} by {self.farmer.user.username}"

# ChatRoom for negotiations


class ChatRoom(models.Model):
    farmer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chatrooms_as_farmer")
    buyer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chatrooms_as_buyer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.buyer.user.username} and {self.farmer.user.username}"

# Messages in the ChatRoom


class ChatMessage(models.Model):
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user.username}"

# Bidding model


class Bid(models.Model):
    listing = models.ForeignKey(
        FarmerListing, on_delete=models.CASCADE, related_name="bids")
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.buyer.user.username} on {self.listing.crop_name}"

# Agreement model for smart contracts


class Agreement(models.Model):
    chatroom = models.OneToOneField(ChatRoom, on_delete=models.CASCADE)
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2)
    signed_at = models.DateTimeField(null=True, blank=True)
    is_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Agreement for {self.chatroom.farmer.user.username} and {self.chatroom.buyer.user.username}"
