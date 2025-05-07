from django.contrib import admin
from .models import Order, Payout

# Register your models here.
admin.site.register(Order)
admin.site.register(Payout)
