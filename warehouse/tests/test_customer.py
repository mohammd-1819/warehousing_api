from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from warehouse.models import Customer
from account.models import User


class CategoryViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(email='testuser', password='testpass')
        cls.admin_user = User.objects.create_superuser(email='admin', password='adminpass')
        cls.customer = Customer.objects.create(user=cls.user, full_name='testfullname', email='test@gmail.com',
                                               phone=12345676789)

    def setUp(self):
        # jwt for users
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_customer_list_view(self):
        url = reverse('warehouse:customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_warehouse_detail_view(self):
        url = reverse('warehouse:customer-detail', kwargs={'pk': self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_update_view(self):
        # jwt for admin users
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:customer-update', kwargs={'pk': self.customer.id})
        response = self.client.put(url, {'full_name': 'updated fullname'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_delete_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:customer-delete', kwargs={'pk': self.customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_create_view(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('warehouse:customer-create')
        data = {'user': self.customer.user.id, 'full_name': self.customer.full_name, 'email': self.customer.email,
                'phone': self.customer.phone}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
