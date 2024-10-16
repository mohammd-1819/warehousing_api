from warehouse.models import Warehouse
from warehouse.serializers import WarehouseSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from warehouse.pagination import StandardResultSetPagination
from warehouse.permissions import IsReadOnlyUser


class WarehouseListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        warehouses = Warehouse.objects.all()
        result = self.paginate_queryset(warehouses, request)
        serializer = WarehouseSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class WarehouseDetailView(APIView):

    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse, id=pk)
        serializer = WarehouseSerializer(instance=warehouse)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WarehouseUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        warehouse = get_object_or_404(Warehouse, id=pk)
        serializer = WarehouseSerializer(instance=warehouse, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        stock = get_object_or_404(Warehouse, id=pk)
        stock.delete()
        return Response({'response': 'stock removed'})


class WarehouseCreateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
