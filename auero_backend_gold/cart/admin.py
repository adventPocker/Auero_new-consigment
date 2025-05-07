from django.contrib import admin
from .models import Cart, CartItem, GuestCart, GuestCartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('product', 'quantity', 'added_at')
    readonly_fields = ('added_at',)
    autocomplete_fields = ['product']

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

class GuestCartItemInline(admin.TabularInline):
    model = GuestCartItem
    extra = 1
    fields = ('product', 'quantity', 'added_at')
    readonly_fields = ('added_at',)
    autocomplete_fields = ['product']

class GuestCartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'created_at', 'updated_at')
    search_fields = ('session_key',)
    inlines = [GuestCartItemInline]
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Cart, CartAdmin)
admin.site.register(GuestCart, GuestCartAdmin)
