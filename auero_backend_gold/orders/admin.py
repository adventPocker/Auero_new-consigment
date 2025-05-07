from django.contrib import admin
from .models import Order, Payout

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'vendor', 'sale_price', 'sale_date', 'payout_status', 'payout')
    list_filter = ('payout_status', 'sale_date', 'vendor', 'buyer')
    search_fields = ('id', 'product__name', 'buyer__username', 'vendor__username')
    autocomplete_fields = ['product', 'buyer', 'vendor', 'payout']
    readonly_fields = ('sale_date',)

class PayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'vendor', 'amount', 'date', 'method')
    list_filter = ('date', 'vendor', 'method')
    search_fields = ('id', 'product__name', 'vendor__username', 'method')
    autocomplete_fields = ['product', 'vendor']
    readonly_fields = ('date',)

admin.site.unregister(Order) if admin.site.is_registered(Order) else None
admin.site.unregister(Payout) if admin.site.is_registered(Payout) else None
admin.site.register(Order, OrderAdmin)
admin.site.register(Payout, PayoutAdmin)
