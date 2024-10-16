from warehouse.models import Stock
from warehouse.serializers import StockSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from warehouse.pagination import StandardResultSetPagination
from warehouse.permissions import IsReadOnlyUser


class StockListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        stocks = Stock.objects.all()
        result = self.paginate_queryset(stocks, request)
        serializer = StockSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class StockDetailView(APIView):

    def get(self, request, pk):
        stock = get_object_or_404(Stock, id=pk)
        serializer = StockSerializer(instance=stock)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StockUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        stock = get_object_or_404(Stock, id=pk)
        serializer = StockSerializer(instance=stock, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        stock = get_object_or_404(Stock, id=pk)
        stock.delete()
        return Response({'response': 'stock removed'})


class StockCreateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
