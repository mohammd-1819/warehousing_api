from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from warehouse.models import Stock, Category, Supplier, Product, Warehouse
from account.models import User


class CategoryViewTests(APITestCase):

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
            product_id= '1234132'
        )
        cls.warehouse = Warehouse.objects.create(name='testwarehouse', location='testlocation')
        cls.stock = Stock.objects.create(product=cls.product, warehouse=cls.warehouse, quantity=12)

    def setUp(self):
        # jwt for users
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_stock_list_view(self):
        url = reverse('warehouse:stock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stock_detail_view(self):
        url = reverse('warehouse:stock-detail', kwargs={'pk': self.stock.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stock_update_view(self):
        # jwt for admin users
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:stock-update', kwargs={'pk': self.stock.id})
        response = self.client.put(url, {'quantity': 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stock_delete_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:stock-delete', kwargs={'pk': self.stock.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stock_create_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:stock-create')
        data = {'product': self.product.name, 'warehouse': self.warehouse.name, 'quantity': 15}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
