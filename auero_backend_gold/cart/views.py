from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, GuestCart, GuestCartItem
from .serializers import CartSerializer, CartItemSerializer, GuestCartSerializer, GuestCartItemSerializer
from products.models import Product
from authentication.models import CustomUser

# Create your views here.

# User Cart Views
class UserCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class UserCartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class UserCartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if item:
            item.delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class UserCartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if item:
            item.quantity = quantity
            item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class UserCartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

# Guest Cart Views
class GuestCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        session_key = request.query_params.get('session_key')
        if not session_key:
            return Response({'error': 'session_key required'}, status=400)
        cart, _ = GuestCart.objects.get_or_create(session_key=session_key)
        serializer = GuestCartSerializer(cart)
        return Response(serializer.data)

class GuestCartAddView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_key = request.data.get('session_key')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        if not session_key or not product_id:
            return Response({'error': 'session_key and product_id required'}, status=400)
        cart, _ = GuestCart.objects.get_or_create(session_key=session_key)
        product = get_object_or_404(Product, id=product_id)
        item, created = GuestCartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        serializer = GuestCartSerializer(cart)
        return Response(serializer.data)

class GuestCartRemoveView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_key = request.data.get('session_key')
        product_id = request.data.get('product_id')
        if not session_key or not product_id:
            return Response({'error': 'session_key and product_id required'}, status=400)
        cart = GuestCart.objects.filter(session_key=session_key).first()
        if cart:
            item = GuestCartItem.objects.filter(cart=cart, product_id=product_id).first()
            if item:
                item.delete()
        serializer = GuestCartSerializer(cart) if cart else None
        return Response(serializer.data if serializer else {})

class GuestCartUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_key = request.data.get('session_key')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        if not session_key or not product_id:
            return Response({'error': 'session_key and product_id required'}, status=400)
        cart = GuestCart.objects.filter(session_key=session_key).first()
        if cart:
            item = GuestCartItem.objects.filter(cart=cart, product_id=product_id).first()
            if item:
                item.quantity = quantity
                item.save()
        serializer = GuestCartSerializer(cart) if cart else None
        return Response(serializer.data if serializer else {})

class GuestCartClearView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_key = request.data.get('session_key')
        if not session_key:
            return Response({'error': 'session_key required'}, status=400)
        cart = GuestCart.objects.filter(session_key=session_key).first()
        if cart:
            cart.items.all().delete()
        serializer = GuestCartSerializer(cart) if cart else None
        return Response(serializer.data if serializer else {})

# Merge Guest Cart into User Cart
class CartMergeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_key = request.data.get('session_key')
        if not session_key:
            return Response({'error': 'session_key required'}, status=400)
        guest_cart = GuestCart.objects.filter(session_key=session_key).first()
        if not guest_cart:
            return Response({'error': 'Guest cart not found'}, status=404)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        for guest_item in guest_cart.items.all():
            item, created = CartItem.objects.get_or_create(cart=user_cart, product=guest_item.product)
            if not created:
                item.quantity += guest_item.quantity
            else:
                item.quantity = guest_item.quantity
            item.save()
        guest_cart.delete()
        serializer = CartSerializer(user_cart)
        return Response(serializer.data)
