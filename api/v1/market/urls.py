from django.urls import path
from market.views import search_buyers, search_farmers, create_auction, list_auctions, submit_bid, accept_bid

urlpatterns = [
    path('search-buyer/', search_buyers, name='search_buyers'),
    path('search-farmer/', search_farmers, name='search_farmers'),
    path('create-auction/', create_auction, name='create_auction'),
    path('list-auctions/', list_auctions, name='list_auctions'),
    path('submit-bid/', submit_bid, name='submit_bid'),
    path('accept-bid/', accept_bid, name='accept_bid'),
]
