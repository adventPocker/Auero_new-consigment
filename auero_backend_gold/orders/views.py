from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order, Payout
from .serializers import OrderSerializer, PayoutSerializer
from products.models import Product
from authentication.models import CustomUser

# Create your views here.

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id=None):
        # If order_id is provided, return details for that specific order
        if order_id:
            order = self.get_order_object(order_id, request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        
        # Otherwise, return a list of orders based on user role
        if request.user.is_staff:
            orders = Order.objects.all()
        elif hasattr(request.user, 'user_type') and request.user.user_type == 'vendor':
            orders = Order.objects.filter(vendor=request.user)
        else:
            orders = Order.objects.filter(buyer=request.user)
            
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
        
    def get_order_object(self, order_id, user):
        order = get_object_or_404(Order, id=order_id)
        # Check permissions: staff can see all, vendors can see their orders, buyers can see their purchases
        if not user.is_staff and user != order.vendor and user != order.buyer:
            raise PermissionError("Not authorized to access this order")
        return order

class PayoutListView(APIView):
  

    def get(self, request, payout_id=None):
        # If payout_id is provided, return details for that specific payout
        if payout_id:
            payout = self.get_payout_object(payout_id, request.user)
            serializer = PayoutSerializer(payout)
            return Response(serializer.data)
            
        # Otherwise, return a list of payouts based on user role
        if request.user.is_staff:
            payouts = Payout.objects.all()
        else:
            payouts = Payout.objects.filter(vendor=request.user)
            
        serializer = PayoutSerializer(payouts, many=True)
        return Response(serializer.data)
        
    def get_payout_object(self, payout_id, user):
        payout = get_object_or_404(Payout, id=payout_id)
        # Check permissions: staff can see all, vendors can only see their payouts
        if not user.is_staff and user != payout.vendor:
            raise PermissionError("Not authorized to access this payout")
        return payout

class MarkPayoutPaidView(APIView):
    

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.payout_status == 'PAID':
            return Response({'detail': 'Already paid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create payout record
        payout = Payout.objects.create(
            product=order.product,
            vendor=order.vendor,
            amount=order.product.vendor_payout or order.sale_price,
            method=request.data.get('method', ''),
            notes=request.data.get('notes', '')
        )
        
        order.payout = payout
        order.payout_status = 'PAID'
        order.save()
        
        # Update product payout_status
        order.product.payout_status = 'PAID'
        order.product.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
