from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from warehouse.models import Product, Category, Supplier
from account.models import User


class ProductViewTests(APITestCase):

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

    def setUp(self):
        # jwt for users
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_product_list_view(self):
        url = reverse('warehouse:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_view(self):
        url = reverse('warehouse:product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_product_update_view(self):
        # jwt for admin users
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse('warehouse:product-update', kwargs={'pk': self.product.id})
        response = self.client.put(url, {'name': 'Updated Product'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')

    def test_product_delete_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse('warehouse:product-delete', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:product-create')
        data = {'name': 'New Product', 'price': 15, 'category': self.category.title, 'supplier': self.supplier.name,
                'description': 'test description', 'product_id': '23123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
