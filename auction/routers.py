# auction/routers.py
from django.urls import re_path,path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/auction/(?P<product_id>\d+)/$', ChatConsumer.as_asgi()),
    # re_path(r'ws/auction/(?P<product_id>\d+)/$', AuctionConsumer.as_asgi()),
    # path("ws/auction/<product_id>", AuctionConsumer.as_asgi()),
    # re_path(r'ws/socket-server/', ChatConsumer.as_asgi()),
    # path('ws/socket-server/', ChatConsumer.as_asgi()),
    # path('ws/auction/<product_id>', ChatConsumer.as_asgi()),
]
