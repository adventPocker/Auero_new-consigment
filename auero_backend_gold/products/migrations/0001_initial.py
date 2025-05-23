# Generated by Django 5.1.7 on 2025-05-07 17:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_ar', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('description_ar', models.TextField(blank=True)),
                ('banner_image', models.ImageField(blank=True, null=True, upload_to='category_banners/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('name_ar', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('description_ar', models.TextField()),
                ('vendor_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('platform_fee', models.DecimalField(blank=True, decimal_places=2, help_text='Fee taken by platform', max_digits=12, null=True)),
                ('vendor_payout', models.DecimalField(blank=True, decimal_places=2, help_text='Amount to be paid to vendor after sale', max_digits=12, null=True)),
                ('payout_status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING', help_text='Whether vendor has been paid', max_length=20)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('INSPECTION', 'Under Inspection'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('SOLD', 'Sold')], default='DRAFT', max_length=20)),
                ('inspection_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConsignmentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handover_date', models.DateTimeField(blank=True, null=True)),
                ('inspection_date', models.DateTimeField(blank=True, null=True)),
                ('physical_status', models.CharField(choices=[('PENDING', 'Pending Delivery'), ('DELIVERED', 'Delivered to Admin'), ('INSPECTED', 'Inspection Complete'), ('RETURNED', 'Returned to Vendor'), ('SOLD', 'Sold to Customer')], default='PENDING', max_length=20)),
                ('quality_notes', models.TextField(blank=True)),
                ('authentication_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inspections', to=settings.AUTH_USER_MODEL)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consignment', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('is_primary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'ordering': ['-is_primary', 'created_at'],
            },
        ),
    ]
