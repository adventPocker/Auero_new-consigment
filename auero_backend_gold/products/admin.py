from django.contrib import admin
from .models import Category, Product, ProductImage, ConsignmentDetails

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['created_at']

class ConsignmentDetailsInline(admin.StackedInline):
    model = ConsignmentDetails
    can_delete = False
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_ar', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_ar', 'slug', 'is_active')
        }),
        ('Description', {
            'fields': ('description', 'description_ar')
        }),
        ('Images', {
            'fields': ('image', 'banner_image')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'category', 'vendor_price', 'selling_price', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'payout_status']
    search_fields = ['name', 'name_ar', 'description', 'vendor__username', 'vendor__email']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    inlines = [ProductImageInline, ConsignmentDetailsInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_ar', 'slug', 'vendor', 'category', 'status')
        }),
        ('Description', {
            'fields': ('description', 'description_ar')
        }),
        ('Pricing', {
            'fields': ('vendor_price', 'selling_price', 'platform_fee', 'vendor_payout', 'payout_status')
        }),
        ('Inspection', {
            'fields': ('inspection_notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']
    readonly_fields = ['created_at']

@admin.register(ConsignmentDetails)
class ConsignmentDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'physical_status', 'handover_date', 'inspection_date', 'inspector']
    list_filter = ['physical_status', 'handover_date', 'inspection_date']
    search_fields = ['product__name', 'quality_notes', 'authentication_notes']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product Information', {
            'fields': ('product',)
        }),
        ('Status', {
            'fields': ('physical_status',)
        }),
        ('Dates', {
            'fields': ('handover_date', 'inspection_date')
        }),
        ('Inspection Details', {
            'fields': ('inspector', 'quality_notes', 'authentication_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )