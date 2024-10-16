from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from warehouse.models import Supplier
from account.models import User


class CategoryViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(email='testuser', password='testpass')
        cls.admin_user = User.objects.create_superuser(email='admin', password='adminpass')
        cls.supplier = Supplier.objects.create(name='testsupplier', email='supplier@gmail.com', phone=2334232)

    def setUp(self):
        # jwt for users
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_supplier_list_view(self):
        url = reverse('warehouse:supplier-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_view(self):
        url = reverse('warehouse:supplier-detail', kwargs={'pk': self.supplier.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_update_view(self):
        # jwt for admin users
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:supplier-update', kwargs={'pk': self.supplier.id})
        response = self.client.put(url, {'name': 'updated supplier'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_delete_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:supplier-delete', kwargs={'pk': self.supplier.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_create_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:supplier-create')
        data = {'name': self.supplier.name, 'email': self.supplier.email, 'phone': self.supplier.phone}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
