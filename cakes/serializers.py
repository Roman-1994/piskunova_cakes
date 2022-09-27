from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import serializers
from cakes.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class StorageFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageFood
        fields = '__all__'


class StorageAdditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageAdditions
        fields = '__all__'


class IngredientsFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsFood
        fields = '__all__'


class DessertsSerializer(serializers.ModelSerializer):
    cost_price = serializers.SerializerMethodField()

    class Meta:
        model = Desserts
        fields = '__all__'

    def get_cost_price(self, obj):
        price_food = sum([int(i.price) for i in obj.ing_food.all()])
        price_add = sum([int(i.price) for i in obj.ing_add.all()])
        return price_food+price_add

    #def to_representation(self, instance):
    #    return instance.fd

