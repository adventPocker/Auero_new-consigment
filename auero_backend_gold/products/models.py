from django.db import models
from django.utils.text import slugify
from authentication.models import CustomUser
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)  # Arabic name
    description = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)  # Arabic description
    banner_image = models.ImageField(upload_to='category_banners/', blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Auto-generated fields
    slug = models.SlugField(unique=True, editable=False,blank=True)  # Auto-generated from name
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Product(models.Model):
    SUBMISSION_STATUS = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('INSPECTION', 'Under Inspection'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('SOLD', 'Sold'),
    ]
    
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)  # Arabic name
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField()
    description_ar = models.TextField()  # Arabic description
    vendor_price = models.DecimalField(max_digits=12, decimal_places=2)  # Vendor's expected price
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Admin-set price
    # Fee sharing fields
    platform_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='Fee taken by platform')
    vendor_payout = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='Amount to be paid to vendor after sale')
    payout_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING', help_text='Whether vendor has been paid')
    status = models.CharField(max_length=20, choices=SUBMISSION_STATUS, default='DRAFT')
    inspection_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'created_at']

class ConsignmentDetails(models.Model):
    PHYSICAL_STATUS = [
        ('PENDING', 'Pending Delivery'),
        ('DELIVERED', 'Delivered to Admin'),
        ('INSPECTED', 'Inspection Complete'),
        ('RETURNED', 'Returned to Vendor'),
        ('SOLD', 'Sold to Customer'),
    ]
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='consignment')
    handover_date = models.DateTimeField(null=True, blank=True)
    inspection_date = models.DateTimeField(null=True, blank=True)
    physical_status = models.CharField(max_length=20, choices=PHYSICAL_STATUS, default='PENDING')
    inspector = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspections')
    quality_notes = models.TextField(blank=True)
    authentication_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Consignment for {self.product.name}"