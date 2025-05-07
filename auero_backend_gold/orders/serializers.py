from rest_framework import serializers
from .models import Order, Payout
from products.serializers import ProductSerializer
from authentication.serializers import UserSerializer

class PayoutSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payout
        fields = [
            'id', 'product', 'product_name', 'vendor', 'vendor_name',
            'amount', 'date', 'method', 'notes'
        ]
    
    def get_vendor_name(self, obj):
        return obj.vendor.get_full_name() if obj.vendor else None
    
    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

class OrderSerializer(serializers.ModelSerializer):
    buyer_details = serializers.SerializerMethodField()
    vendor_details = serializers.SerializerMethodField()
    product_details = serializers.SerializerMethodField()
    payout_details = PayoutSerializer(source='payout', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'product', 'product_details', 'buyer', 'buyer_details',
            'vendor', 'vendor_details', 'sale_price', 'sale_date',
            'payout_status', 'payout', 'payout_details'
        ]
    
    def get_buyer_details(self, obj):
        if not obj.buyer:
            return None
        return {
            'id': obj.buyer.id,
            'username': obj.buyer.username,
            'email': obj.buyer.email,
            'full_name': obj.buyer.get_full_name()
        }
    
    def get_vendor_details(self, obj):
        if not obj.vendor:
            return None
        return {
            'id': obj.vendor.id,
            'username': obj.vendor.username,
            'email': obj.vendor.email,
            'full_name': obj.vendor.get_full_name()
        }
    
    def get_product_details(self, obj):
        if not obj.product:
            return None
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'vendor_price': obj.product.vendor_price,
            'selling_price': obj.product.selling_price,
            'platform_fee': obj.product.platform_fee,
            'vendor_payout': obj.product.vendor_payout
        } 