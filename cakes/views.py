from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from cakes.models import *
from cakes.serializers import *
from .service import *


class UserViewSet(viewsets.ModelViewSet):
    """список пользователей CRUD"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """список групп CRUD"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]


class StorageFoodViewSet(viewsets.ModelViewSet):
    """список продуктов CRUD"""
    queryset = Group.objects.all()
    serializer_class = StorageFoodSerializer


class StorageAdditionsViewSet(viewsets.ModelViewSet):
    """список продуктов CRUD"""
    queryset = Group.objects.all()
    serializer_class = StorageAdditionsSerializer


class DessertsViewSet(viewsets.ModelViewSet):
    """список десертов CRUD"""
    queryset = Desserts.objects.filter(is_active=True)
    serializer_class = DessertsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DessertsFilter
    pagination_class = DessertsPagination


class IngredientsFoodViewSet(viewsets.ModelViewSet):
    """список ингредиентов продуктов CRUD"""
    queryset = IngredientsFood.objects.all()
    serializer_class = IngredientsFoodSerializer


class IngredientsAdditionsViewSet(viewsets.ModelViewSet):
    """список ингредиентов дополнений CRUD"""
    queryset = IngredientsAdditions.objects.all()
    serializer_class = IngredientsAdditionsSerializer


class DecorsViewSet(viewsets.ModelViewSet):
    """список декоров CRUD"""
    queryset = Decor.objects.filter(is_active=True)
    serializer_class = DecorSerializer

