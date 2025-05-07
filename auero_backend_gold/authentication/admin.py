from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VendorProfile
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'user_type')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'profile_image'),
        }),
    )
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'user_type')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_type', 'company_name', 'approved', 'country')
    search_fields = ('user__username', 'company_name', 'business_name')
    list_filter = ('vendor_type', 'approved', 'country')

admin.site.register(VendorProfile, VendorProfileAdmin)
