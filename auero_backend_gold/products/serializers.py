from rest_framework import serializers
from .models import Category, Product, ProductImage, ConsignmentDetails
from authentication.models import CustomUser

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'name_ar', 'slug', 'description', 'description_ar',
            'banner_image', 'image', 'parent', 'is_active', 'created_at', 'updated_at'
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']

class ConsignmentDetailsSerializer(serializers.ModelSerializer):
    inspector_name = serializers.SerializerMethodField()

    class Meta:
        model = ConsignmentDetails
        fields = [
            'id', 'handover_date', 'inspection_date', 'physical_status',
            'inspector', 'inspector_name', 'quality_notes', 'authentication_notes',
            'created_at', 'updated_at'
        ]

    def get_inspector_name(self, obj):
        return obj.inspector.get_full_name() if obj.inspector else None

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    consignment = ConsignmentDetailsSerializer(read_only=True)
    category_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'category', 'category_name',
            'name', 'name_ar', 'slug', 'description', 'description_ar',
            'vendor_price', 'selling_price', 'platform_fee', 'vendor_payout', 'payout_status', 'status', 'inspection_notes',
            'created_at', 'updated_at', 'images', 'consignment'
        ]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_vendor_name(self, obj):
        return obj.vendor.get_full_name() if obj.vendor else None 