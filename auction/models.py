from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    current_bid = models.ForeignKey(
        'Bid', on_delete=models.SET_NULL, null=True, blank=True, related_name='products_as_current_bid')
    end_time = models.DateTimeField(default=timezone.now)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()
