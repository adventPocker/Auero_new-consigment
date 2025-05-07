from django.db import models
from authentication.models import CustomUser
from products.models import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases')
    vendor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    payout_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING')
    payout = models.OneToOneField('Payout', on_delete=models.SET_NULL, null=True, blank=True, related_name='order')

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"

class Payout(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payouts')
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100, blank=True, null=True, help_text='Payment method (e.g., bank transfer, cash)')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payout #{self.id} to {self.vendor.username} for {self.product.name}"
