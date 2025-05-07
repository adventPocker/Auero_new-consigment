from django.urls import path
from .views import OrderListView, PayoutListView, MarkPayoutPaidView

urlpatterns = [
    # Order endpoints
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderListView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/mark-paid/', MarkPayoutPaidView.as_view(), name='mark-payout-paid'),
    
    # Payout endpoints
    path('payouts/', PayoutListView.as_view(), name='payout-list'),
    path('payouts/<int:payout_id>/', PayoutListView.as_view(), name='payout-detail'),
] 