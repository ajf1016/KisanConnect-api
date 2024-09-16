# auction/urls.py
from django.urls import path
from auction.views import ProductListAPIView, product_detail, place_bid

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('products/<int:product_id>/bid/', place_bid, name='place_bid'),
]
