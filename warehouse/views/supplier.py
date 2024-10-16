from warehouse.models import Supplier
from warehouse.serializers import SupplierSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from warehouse.pagination import StandardResultSetPagination
from warehouse.permissions import IsReadOnlyUser


class SupplierListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        suppliers = Supplier.objects.all()
        result = self.paginate_queryset(suppliers, request)
        serializer = SupplierSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class SupplierDetailView(APIView):

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, id=pk)
        serializer = SupplierSerializer(instance=supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        stock = get_object_or_404(Supplier, id=pk)
        serializer = SupplierSerializer(instance=stock, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        stock = get_object_or_404(Supplier, id=pk)
        stock.delete()
        return Response({'response': 'supplier removed'})


class SupplierCreateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
