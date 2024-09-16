from django.contrib import admin
from .models import Bid, Product

# Bring forth the magical items and bids into our grand chamber.
admin.site.register(Product)
admin.site.register(Bid)
