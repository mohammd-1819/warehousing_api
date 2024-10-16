from django.urls import path
from .views import product_category, customer, stock, warehouse, supplier, order

app_name = 'warehouse'

urlpatterns = [
    path('product/list', product_category.ProductListView.as_view(), name='product-list'),
    path('product/detail/<int:pk>', product_category.ProductDetailView.as_view(), name='product-detail'),
    path('product/update/<int:pk>', product_category.ProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>', product_category.ProductDeleteView.as_view(), name='product-delete'),
    path('product/create', product_category.ProductCreateView.as_view(), name='product-create'),

    path('category/list', product_category.CategoryListView.as_view(), name='category-list'),
    path('category/detail/<int:pk>', product_category.CategoryDetailView.as_view(), name='category-detail'),
    path('category/update/<int:pk>', product_category.CategoryUpdateView.as_view(), name='category-update'),
    path('category/delete/<int:pk>', product_category.CategoryDeleteView.as_view(), name='category-delete'),
    path('category/create', product_category.CategoryCreateView.as_view(), name='category-create'),

    path('customer/list', customer.CustomerListView.as_view(), name='customer-list'),
    path('customer/detail/<int:pk>', customer.CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/update/<int:pk>', customer.CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/delete/<int:pk>', customer.CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer/create', customer.CustomerCreateView.as_view(), name='customer-create'),

    path('stock/list', stock.StockListView.as_view(), name='stock-list'),
    path('stock/detail/<int:pk>', stock.StockDetailView.as_view(), name='stock-detail'),
    path('stock/update/<int:pk>', stock.StockUpdateView.as_view(), name='stock-update'),
    path('stock/delete/<int:pk>', stock.StockDeleteView.as_view(), name='stock-delete'),
    path('stock/create', stock.StockCreateView.as_view(), name='stock-create'),

    path('list', warehouse.WarehouseListView.as_view(), name='warehouse-list'),
    path('detail/<int:pk>', warehouse.WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('update/<int:pk>', warehouse.WarehouseUpdateView.as_view(), name='warehouse-update'),
    path('delete/<int:pk>', warehouse.WarehouseDeleteView.as_view(), name='warehouse-delete'),
    path('create', warehouse.WarehouseCreateView.as_view(), name='warehouse-create'),

    path('supplier/list', supplier.SupplierListView.as_view(), name='supplier-list'),
    path('supplier/detail/<int:pk>', supplier.SupplierDetailView.as_view(), name='supplier-detail'),
    path('supplier/update/<int:pk>', supplier.SupplierUpdateView.as_view(), name='supplier-update'),
    path('supplier/delete/<int:pk>', supplier.SupplierDeleteView.as_view(), name='supplier-delete'),
    path('supplier/create', supplier.SupplierCreateView.as_view(), name='supplier-create'),

    path('order', order.OrderView.as_view(), name='order'),
    path('order/detail/<int:pk>', order.OrderDetailView.as_view(), name='order-detail'),
    path('order/update/<int:pk>', order.OrderUpdateView.as_view(), name='order-update'),
    path('order/delete/<int:pk>', order.OrderDeleteView.as_view(), name='order-delete'),

]
