from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from .models import Desserts


class DessertsPagination(PageNumberPagination):
    """Пагинатор десертов"""
    page_size = 2


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class DessertsFilter(filters.FilterSet):
    """Фильтр десертов"""
    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    decor = CharFilterInFilter(field_name='decor__name', lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Desserts
        fields = ['name', 'decor', 'price']

