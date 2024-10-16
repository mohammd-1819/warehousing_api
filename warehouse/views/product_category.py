from warehouse.models import Product, Category, Order
from warehouse.serializers import CategorySerializer, ProductSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from warehouse.pagination import StandardResultSetPagination
from warehouse.permissions import IsReadOnlyUser


class ProductListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        products = Product.objects.all()
        result = self.paginate_queryset(products, request)
        serializer = ProductSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({'response': 'product removed'})


class ProductCreateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------------------

class CategoryListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        categories = Category.objects.all()
        result = self.paginate_queryset(categories, request)
        serializer = CategorySerializer(instance=result, many=True)
        return self.get_paginated_response(serializer.data)


class CategoryDetailView(APIView):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(instance=category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryUpdateView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def put(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def delete(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response({'response': 'category removed'})


class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

