from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
]