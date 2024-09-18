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


class Auction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    variety_of_crop = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction by {self.buyer.username} for {self.crop_name}"


class Bid(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    bidder_name = models.CharField(max_length=100)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.bidder_name} - {self.bid_amount}'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

    def deposit(self, amount):
        """Method to add funds to the wallet."""
        if amount > 0:
            self.balance += amount
            self.save()

    def withdraw(self, amount):
        """Method to withdraw funds from the wallet."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient funds or invalid amount.")


class Escrow(models.Model):
    # Adjust based on your Bid model
    bid = models.ForeignKey('Bid', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # e.g., 'pending', 'completed', 'released'
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Escrow for Bid {self.bid.id}: {self.amount}"
