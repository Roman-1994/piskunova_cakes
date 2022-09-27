from django.contrib.auth.models import User, Group
from rest_framework import serializers
from cakes.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор групп"""
    class Meta:
        model = Group
        fields = ['url', 'name']


class StorageFoodSerializer(serializers.ModelSerializer):
    """Сериализатор склада продуктов"""
    class Meta:
        model = StorageFood
        fields = '__all__'


class StorageAdditionsSerializer(serializers.ModelSerializer):
    """Сериализатор склада дополнений"""
    class Meta:
        model = StorageAdditions
        fields = '__all__'


class IngredientsFoodSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиетов продуктов"""
    class Meta:
        model = IngredientsFood
        fields = '__all__'


class IngredientsAdditionsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиетов дополнений"""
    class Meta:
        model = IngredientsAdditions
        fields = '__all__'


class DessertsSerializer(serializers.ModelSerializer):
    """Сериализатор десертов"""
    cost_price = serializers.SerializerMethodField()

    class Meta:
        model = Desserts
        fields = '__all__'

    """Функция нахождения себестоимости десерта"""
    def get_cost_price(self, obj):
        price_food = sum([int(i.price) for i in obj.ing_food.all()])
        price_add = sum([int(i.price) for i in obj.ing_add.all()])
        price_decor = 0
        if obj.decor:
            price_decor_food = 0
            price_decor_add = 0
            if obj.decor.ing_food:
                price_decor_food = int(obj.decor.ing_food.price)
            if obj.decor.ing_add:
                price_decor_add = int(obj.decor.ing_add.price)
            price_decor = price_decor_food + price_decor_add
        return price_food + price_add + price_decor


class DecorSerializer(serializers.ModelSerializer):
    """Сериализатор декоров"""
    cost_price_decor = serializers.SerializerMethodField()

    class Meta:
        model = Decor
        fields = '__all__'

    """Функция нахождения себестоимости декора"""
    def get_cost_price_decor(self, obj):
        price_food = 0
        price_add = 0
        if obj.ing_food:
            price_food = int(obj.ing_food.price)
        if obj.ing_add:
            price_add = int(obj.ing_add.price)
        return price_food + price_add

