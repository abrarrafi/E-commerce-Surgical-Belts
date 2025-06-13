from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('product-list/', product_list, name='product_list'),
    path('product/<slug:slug>/', product_view, name='product'),
    path('cart/', cart_view, name='cart'),
# use product_name (str) instead of product_id (int)
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),

]
