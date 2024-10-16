from warehouse.models import Order, Stock
from warehouse.serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from warehouse.pagination import StandardResultSetPagination
from warehouse.permissions import IsReadOnlyUser


class OrderView(APIView, StandardResultSetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        result = self.paginate_queryset(orders, request)
        serializer = OrderSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            warehouse = serializer.validated_data['warehouse']
            quantity = serializer.validated_data['quantity']

            stock = Stock.objects.get(product=product, warehouse=warehouse)
            if stock.quantity >= quantity:
                stock.quantity -= quantity
                stock.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif not stock:
                return Response({'error': 'Stock for this product does not exist'})
            else:
                return Response({'error': 'purchase failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        serializer = OrderSerializer(instance=order, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        order.delete()
        return Response({'response': 'order removed'})
