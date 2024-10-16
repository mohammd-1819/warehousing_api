from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from warehouse.models import Order, Product, Warehouse, Stock, Category, Supplier, Customer


class OrderViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(email='testuser', password='testpass')
        cls.admin_user = User.objects.create_superuser(email='admin', password='adminpass')
        cls.category = Category.objects.create(title='test_cat')
        cls.supplier = Supplier.objects.create(name='testsupplier', email='supplier@gmail.com', phone='2334232')
        cls.product = Product.objects.create(
            name='Test Product',
            price=10,
            category=cls.category,
            supplier=cls.supplier,
            description='test product description',
            product_id='1234132'
        )
        cls.customer = Customer.objects.create(user=cls.user, full_name='testfullname', email='test@gmail.com',
                                               phone=12345676789)
        cls.warehouse = Warehouse.objects.create(name='testwarehouse', location='testlocation')
        cls.stock = Stock.objects.create(product=cls.product, warehouse=cls.warehouse, quantity=12)
        cls.order = Order.objects.create(product=cls.product, warehouse=cls.warehouse, quantity=2, price=50,
                                         customer=cls.customer)

    def setUp(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_order_list_view(self):
        url = reverse('warehouse:order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_create_view(self):
        url = reverse('warehouse:order')
        data = {
            'product': self.product.name,
            'warehouse': self.warehouse.name,
            'quantity': 5,
            'price': self.order.price,
            'customer': self.order.customer.email
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.stock.refresh_from_db()

    def test_order_detail_view(self):
        url = reverse('warehouse:order-detail', kwargs={'pk': self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_update_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:order-update', kwargs={'pk': self.order.id})
        response = self.client.put(url, {'quantity': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()

    def test_order_delete_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:order-delete', kwargs={'pk': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
