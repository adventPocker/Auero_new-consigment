from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ConsignmentDetails
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductImageSerializer,
    ConsignmentDetailsSerializer
)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.

class CategoryList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        # if not request.user.is_staff:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        print(serializer.error_messages)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        # if not request.user.is_staff:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
      
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryProducts(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(vendor=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        product = get_object_or_404(Product, pk=pk)
        if not user.is_staff and product.vendor != user:
            raise PermissionError("Not authorized to access this product")
        return product

    def get(self, request, pk):
        product = self.get_object(pk, request.user)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk, request.user)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            updated_product = serializer.save()
            # Fee sharing logic: calculate on sale
            if updated_product.status == 'SOLD':
                if updated_product.selling_price and (updated_product.platform_fee is None or updated_product.vendor_payout is None):
                    platform_fee = updated_product.selling_price * 0.10  # 10% platform fee
                    vendor_payout = updated_product.selling_price - platform_fee
                    updated_product.platform_fee = platform_fee
                    updated_product.vendor_payout = vendor_payout
                    updated_product.save()
            return Response(ProductSerializer(updated_product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk, request.user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductImages(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.is_staff and product.vendor != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        images = request.FILES.getlist('images')
        is_primary = request.data.get('is_primary', False)

        if not images:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_images = []
        for image in images:
            should_be_primary = is_primary or not ProductImage.objects.filter(product=product).exists()
            product_image = ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=should_be_primary
            )
            serializer = ProductImageSerializer(product_image)
            uploaded_images.append(serializer.data)

        return Response(uploaded_images, status=status.HTTP_201_CREATED)

class ConsignmentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            consignments = ConsignmentDetails.objects.all()
        else:
            consignments = ConsignmentDetails.objects.filter(product__vendor=request.user)
        serializer = ConsignmentDetailsSerializer(consignments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsignmentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_staff:
                serializer.save(inspector=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsignmentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        consignment = get_object_or_404(ConsignmentDetails, pk=pk)
        if not user.is_staff and consignment.product.vendor != user:
            raise PermissionError("Not authorized to access this consignment")
        return consignment

    def get(self, request, pk):
        consignment = self.get_object(pk, request.user)
        serializer = ConsignmentDetailsSerializer(consignment)
        return Response(serializer.data)

    def put(self, request, pk):
        consignment = self.get_object(pk, request.user)
        serializer = ConsignmentDetailsSerializer(consignment, data=request.data)
        if serializer.is_valid():
            if request.user.is_staff and 'inspector' not in serializer.validated_data:
                serializer.save(inspector=request.user)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        consignment = self.get_object(pk, request.user)
        consignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConsignmentStatus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        consignment = get_object_or_404(ConsignmentDetails, pk=pk)
        if not request.user.is_staff and consignment.product.vendor != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('physical_status')
        if not new_status:
            return Response(
                {'error': 'Status not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in dict(ConsignmentDetails.PHYSICAL_STATUS):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        consignment.physical_status = new_status
        consignment.save()
        serializer = ConsignmentDetailsSerializer(consignment)
        return Response(serializer.data)

def search_products(
    query=None,
    category=None,
    min_price=None,
    max_price=None,
    status=None,
    ordering=None,
):
    qs = Product.objects.all()
    if query:
        qs = qs.filter(
            Q(name__icontains=query) |
            Q(name_ar__icontains=query) |
            Q(description__icontains=query) |
            Q(description_ar__icontains=query) |
            Q(category__name__icontains=query)
        )
    if category:
        qs = qs.filter(category__id=category)
    if min_price is not None:
        qs = qs.filter(selling_price__gte=min_price)
    if max_price is not None:
        qs = qs.filter(selling_price__lte=max_price)
    if status:
        qs = qs.filter(status=status)
    if ordering:
        qs = qs.order_by(ordering)
    return qs

class ProductSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q')
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        status = request.GET.get('status')
        ordering = request.GET.get('ordering', '-created_at')
        min_price = float(min_price) if min_price else None
        max_price = float(max_price) if max_price else None
        products_qs = search_products(
            query=query,
            category=category,
            min_price=min_price,
            max_price=max_price,
            status=status,
            ordering=ordering,
        )
        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get('page_size', 20))
        result_page = paginator.paginate_queryset(products_qs, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
