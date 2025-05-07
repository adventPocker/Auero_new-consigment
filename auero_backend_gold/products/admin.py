from django.contrib import admin
from .models import Category, Product, ProductImage, ConsignmentDetails
from authentication.models import CustomUser

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary', 'created_at')
    readonly_fields = ('created_at',)

class ConsignmentDetailsInline(admin.StackedInline):
    model = ConsignmentDetails
    extra = 0
    can_delete = False
    fields = ('handover_date', 'inspection_date', 'physical_status', 'inspector', 'quality_notes', 'authentication_notes', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'status', 'vendor_price', 'selling_price', 'platform_fee', 'vendor_payout', 'payout_status', 'created_at')
    list_filter = ('status', 'category', 'vendor', 'payout_status')
    search_fields = ('name', 'vendor__username', 'category__name')
    inlines = [ProductImageInline, ConsignmentDetailsInline]
    fieldsets = (
        (None, {'fields': ('name', 'name_ar', 'slug', 'vendor', 'category', 'description', 'description_ar')}),
        ('Pricing', {'fields': ('vendor_price', 'selling_price', 'platform_fee', 'vendor_payout', 'payout_status')}),
        ('Status', {'fields': ('status', 'inspection_notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('slug', 'created_at', 'updated_at')
    autocomplete_fields = ['vendor', 'category']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If the user is a vendor, only show their products
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(vendor=request.user)

    def save_model(self, request, obj, form, change):
        # Automatically set vendor to current user if not set and user is not staff
        if not obj.vendor_id and not request.user.is_staff and not request.user.is_superuser:
            obj.vendor = request.user
        super().save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'is_active', 'parent', 'created_at')
    search_fields = ('name', 'name_ar')
    list_filter = ('is_active', 'parent')
    readonly_fields = ('slug', 'created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
