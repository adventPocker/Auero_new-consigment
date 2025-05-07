from django.contrib import admin
from .models import Order, Payout

class PayoutInline(admin.TabularInline):
    model = Payout
    extra = 0
    readonly_fields = ['date']
    fields = ['vendor', 'amount', 'method', 'date', 'notes']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'buyer_name', 'vendor_name', 'sale_price', 'sale_date', 'payout_status']
    list_filter = ['payout_status', 'sale_date']
    search_fields = ['product__name', 'buyer__username', 'buyer__email', 'vendor__username', 'vendor__email']
    readonly_fields = ['sale_date']
    fieldsets = (
        ('Order Information', {
            'fields': ('product', 'sale_price', 'sale_date')
        }),
        ('User Information', {
            'fields': ('buyer', 'vendor')
        }),
        ('Payout Information', {
            'fields': ('payout_status', 'payout')
        }),
    )
    
    def product_name(self, obj):
        return obj.product.name if obj.product else 'N/A'
    product_name.short_description = 'Product'
    
    def buyer_name(self, obj):
        return obj.buyer.get_full_name() if obj.buyer else 'N/A'
    buyer_name.short_description = 'Buyer'
    
    def vendor_name(self, obj):
        return obj.vendor.get_full_name() if obj.vendor else 'N/A'
    vendor_name.short_description = 'Vendor'

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'vendor_name', 'amount', 'date', 'method']
    list_filter = ['date', 'method']
    search_fields = ['product__name', 'vendor__username', 'vendor__email', 'method']
    readonly_fields = ['date']
    fieldsets = (
        ('Payout Information', {
            'fields': ('amount', 'date', 'method', 'notes')
        }),
        ('Related Information', {
            'fields': ('product', 'vendor')
        }),
    )
    
    def product_name(self, obj):
        return obj.product.name if obj.product else 'N/A'
    product_name.short_description = 'Product'
    
    def vendor_name(self, obj):
        return obj.vendor.get_full_name() if obj.vendor else 'N/A'
    vendor_name.short_description = 'Vendor'
