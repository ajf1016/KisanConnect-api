from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")

    # Common fields for both farmers and buyers
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    adharcard = models.CharField(max_length=12, unique=True)

    # Fields specific to farmers
    is_farmer = models.BooleanField(default=False)
    acre_of_land = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    kisan_card = models.CharField(max_length=16, null=True, blank=True)

    # Fields specific to buyers
    is_buyer = models.BooleanField(default=False)
    gst = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
