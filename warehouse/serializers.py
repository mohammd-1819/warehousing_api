from rest_framework import serializers
from .models import Category, Product, Order, Supplier, Customer, Stock, Warehouse


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', queryset=Category.objects.all())
    supplier = serializers.SlugRelatedField(slug_field='name', queryset=Supplier.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'product_id', 'price', 'supplier')


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    customer = serializers.SlugRelatedField(slug_field='email', queryset=Customer.objects.all())
    warehouse = serializers.SlugRelatedField(slug_field='name', queryset=Warehouse.objects.all())

    class Meta:
        model = Order
        fields = ('customer', 'product', 'price', 'warehouse', 'quantity')
        read_only_fields = ('created_at',)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name', 'email', 'phone')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user', 'full_name', 'email', 'phone')


class StockSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    warehouse = serializers.SlugRelatedField(slug_field='name', queryset=Warehouse.objects.all())

    class Meta:
        model = Stock
        fields = ('product', 'warehouse', 'quantity')


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('name', 'location')
