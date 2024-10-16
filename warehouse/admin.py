from django.contrib import admin
from . import models


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'price')


admin.site.register(models.Category)
admin.site.register(models.Warehouse)

