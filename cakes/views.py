from django.http import JsonResponse
from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import views
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from cakes.models import *
from cakes.serializers import *


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
    queryset = Desserts.objects.all()
    serializer_class = DessertsSerializer


class IngredientsFoodViewSet(viewsets.ModelViewSet):
    queryset = IngredientsFood.objects.all()
    serializer_class = IngredientsFoodSerializer

