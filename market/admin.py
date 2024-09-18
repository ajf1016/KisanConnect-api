# market/admin.py

from django.contrib import admin
from .models import Auction, Bid, Wallet, Escrow

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Wallet)
admin.site.register(Escrow)
