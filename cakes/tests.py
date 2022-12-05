from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
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
        response = self.client.post(url, self.food, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_additions(self):
        url = reverse('additions')
        response = self.client.post(url, self.additions, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], 'Коробка под капкейки 4шт.')
        self.assertEqual(len(response.data), 1)
