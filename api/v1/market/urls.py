from django.urls import path
from market.views import search_buyers, search_farmers, initiate_chat

urlpatterns = [
    path('search-buyer/', search_buyers, name='search_buyers'),
    path('search-farmer/', search_farmers, name='search_farmers'),
    path('chat/initiate/', initiate_chat, name='initiate_chat'),
]
