from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, VendorProfile, Address

class VendorProfileInline(admin.StackedInline):
    model = VendorProfile
    can_delete = False
    verbose_name_plural = 'Vendor Profile'
    fk_name = 'user'
    extra = 0
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj and obj.user_type != 'vendor':
            return None
        return formset

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('vendor_type') == 'company' and not cleaned_data.get('company_name'):
            raise ValidationError(_('Company name is required for company type vendors.'))
        return cleaned_data

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    min_num = 0
    max_num = 5  # Limit number of addresses per user

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_image')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    inlines = [VendorProfileInline, AddressInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new users
            if obj.user_type == 'vendor' and not hasattr(obj, 'vendor_profile'):
                # Create empty vendor profile for new vendor users
                VendorProfile.objects.create(user=obj)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('vendor_profile')

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_type', 'company_name', 'approved', 'created_at')
    list_filter = ('vendor_type', 'approved', 'created_at')
    search_fields = ('user__username', 'user__email', 'company_name', 'business_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'country', 'created_at')
    list_filter = ('country', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'address_line1', 'city', 'country')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
