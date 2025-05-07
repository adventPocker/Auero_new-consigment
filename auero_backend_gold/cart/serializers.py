from rest_framework import serializers
from .models import Cart, CartItem, GuestCart, GuestCartItem
from products.models import Product
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class GuestCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = GuestCartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']

class GuestCartSerializer(serializers.ModelSerializer):
    items = GuestCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = GuestCart
        fields = ['id', 'session_key', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 