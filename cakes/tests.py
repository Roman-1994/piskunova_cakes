from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .views import *
from datetime import datetime


class DessertsListTestsCase(APITestCase):
    def setUp(self):
        data = {
            'id': 1,
            'name': 'Торт',
            'price': 1000,
            'amount': 1,
            'created_at': datetime.today()
        }
        Desserts.objects.create(**data)

        user_admin = User.objects.create(username='Test', password='Test', is_superuser=True, is_staff=True, is_active=True,
                                         date_joined=datetime.today())
        user_admin.save()
        user_t = User.objects.create(username='Test1', password='Test1', is_superuser=False, is_staff=False, is_active=True,
                                     date_joined=datetime.today())
        user_t.save()

        self.user_admin_token = Token.objects.create(user=user_admin)
        self.user_t_token = Token.objects.create(user=user_t)

        self.f = StorageFood.objects.create(name='Мука', amount=1000, unit_measure='гр.', price=100, min_amount=500)
        self.f.save()

        self.food = {
            'name': 'Сахар',
            'amount': 1000,
            'unit_measure': 'гр.',
            'price': 100,
            'min_amount': 500
        }

        self.additions = {
            'name': 'Коробка под капкейки 4шт.',
            'amount': 10,
            'unit_measure': 'шт.',
            'price': 300,
            'min_amount': 5
        }

        i_f = IngredientsFood.objects.create(name_food=self.f, amount=10, unit_measure='гр.', price=3)
        i_f.save()

        self.factory = APIRequestFactory()
        self.view = DessertsListView.as_view()
        self.url = reverse('desserts_list')

    def test_desserts_list(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_desserts_detail(self):
        url = reverse('desserts_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), 'Торт')

    def test_food(self):
        url = reverse('food')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_admin_token.key)
        response = self.client.post(url, self.food, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_food_invalid_user(self):
        url = reverse('food')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_t_token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_food_invalid(self):
        url = reverse('food')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_additions(self):
        url = reverse('additions')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_admin_token.key)
        response = self.client.post(url, self.additions, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], 'Коробка под капкейки 4шт.')
        self.assertEqual(len(response.data), 1)

    def test_additions_invalid_user(self):
        url = reverse('additions')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_t_token.key)
        response = self.client.post(url, self.additions, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_additions_invalid(self):
        url = reverse('additions')
        response = self.client.post(url, self.additions, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredients_food(self):
        url = reverse('ingfood')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_admin_token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['name_food'], self.f.id)
