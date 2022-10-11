from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from .models import Desserts, Decor


class DessertsPagination(PageNumberPagination):
    """Пагинатор десертов"""
    page_size = 2


class DessertsFilter(filters.FilterSet):
    """Фильтр десертов"""
    name = filters.CharFilter(lookup_expr='icontains')
    decor__name = filters.CharFilter(lookup_expr='icontains')
    price = filters.RangeFilter()
    ing_food__name_food__name = filters.CharFilter(lookup_expr='icontains')
    ing_add__name_addition__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Desserts
        fields = ['name', 'decor', 'price', 'ing_food', 'ing_add']


class DecorsFilter(filters.FilterSet):
    """Фильтр декоров"""
    name = filters.CharFilter(lookup_expr='icontains')

    price = filters.RangeFilter()

    ing_food__name_food__name = filters.CharFilter(lookup_expr='icontains')
    ing_add__name_addition__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Decor
        fields = ['name', 'price', 'ing_food', 'ing_add']

