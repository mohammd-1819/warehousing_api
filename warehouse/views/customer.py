from warehouse.models import Customer
from warehouse.serializers import CustomerSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from warehouse.pagination import StandardResultSetPagination
from warehouse.permissions import IsReadOnlyUser


class CustomerListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        customers = Customer.objects.all()
        result = self.paginate_queryset(customers, request)
        serializer = CustomerSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class CustomerDetailView(APIView):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request, pk):
        customer = get_object_or_404(Customer, id=pk)
        serializer = CustomerSerializer(instance=customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, id=pk)
        serializer = CustomerSerializer(instance=customer, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, id=pk)
        customer.delete()
        return Response({'response': 'Customer removed'})


class CustomerCreateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
