from django.contrib import admin
from .models import Cart, CartItem, GuestCart, GuestCartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']

class GuestCartItemInline(admin.TabularInline):
    model = GuestCartItem
    extra = 0
    readonly_fields = ['added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Number of Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['added_at']

@admin.register(GuestCart)
class GuestCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key', 'item_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_key']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [GuestCartItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Number of Items'

@admin.register(GuestCartItem)
class GuestCartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__session_key', 'product__name']
    readonly_fields = ['added_at']
