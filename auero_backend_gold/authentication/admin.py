from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VendorProfile, Address

class VendorProfileInline(admin.StackedInline):
    model = VendorProfile
    can_delete = False
    verbose_name_plural = 'Vendor Profile'
    fk_name = 'user'

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_image')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [VendorProfileInline, AddressInline]

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_type', 'company_name', 'approved', 'created_at')
    list_filter = ('vendor_type', 'approved', 'created_at')
    search_fields = ('user__username', 'user__email', 'company_name', 'business_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'country', 'created_at')
    list_filter = ('country', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'address_line1', 'city', 'country')
    readonly_fields = ('created_at', 'updated_at')
