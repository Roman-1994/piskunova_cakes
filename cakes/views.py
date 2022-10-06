from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from cakes.models import *
from cakes.serializers import *
from .service import *


class UserViewSet(viewsets.ModelViewSet):
    """список пользователей CRUD"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """список групп CRUD"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class StorageFoodListCreateView(generics.ListCreateAPIView):
    """Вывод списка продуктов"""
    queryset = StorageFood.objects.all()
    serializer_class = StorageFoodSerializer
    permission_classes = [permissions.IsAdminUser]


class StorageAdditionsListCreateView(generics.ListCreateAPIView):
    """Вывод списка дополнений"""
    queryset = StorageAdditions.objects.all()
    serializer_class = StorageAdditionsSerializer
    permission_classes = [permissions.IsAdminUser]


class DessertsListView(generics.ListAPIView):
    """Вывод списка десертов"""
    queryset = Desserts.objects.filter(is_active=True)
    serializer_class = DessertsListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DessertsFilter
    pagination_class = DessertsPagination
    permission_classes = [permissions.AllowAny]


class DessertsDetailView(generics.RetrieveAPIView):
    """Вывод десертa"""
    queryset = Desserts.objects.filter(is_active=True)
    serializer_class = DessertsDetailSerializer
    permission_classes = [permissions.AllowAny]


class IngredientsFoodListView(generics.ListAPIView):
    """Вывод списка ингредиентов продуктов"""
    queryset = IngredientsFood.objects.all()
    serializer_class = IngredientsFoodSerializer
    permission_classes = [permissions.IsAdminUser]


class IngredientsAdditionsListView(generics.ListAPIView):
    """Вывод списка ингредиентов дополнений"""
    queryset = IngredientsAdditions.objects.all()
    serializer_class = IngredientsAdditionsSerializer
    permission_classes = [permissions.IsAdminUser]


class DecorsListView(generics.ListAPIView):
    """Вывод списка декоров"""
    queryset = Decor.objects.filter(is_active=True)
    serializer_class = DecorListSerializer


class DecorsDetailView(generics.RetrieveAPIView):
    """Вывод декора"""
    queryset = Decor.objects.filter(is_active=True)
    serializer_class = DecorDetailSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    """список заказов CRUD"""
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


@api_view(['GET', 'POST'])
def comments(request, pk):
    """Вывод и создание комментариев к десерту"""
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, dessert=pk, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def comments_decor(request, pk):
    """Вывод и создание комментариев к декору"""
    if request.method == 'POST':
        serializer = CommentDecorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = CommentDecor.objects.filter(is_active=True, decor=pk, parent=None)
        serializer = CommentDecorSerializer(comments, many=True)
        return Response(serializer.data)