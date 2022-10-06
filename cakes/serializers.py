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
    message_food = serializers.SerializerMethodField()

    class Meta:
        model = StorageFood
        fields = '__all__'

    def get_message_food(self, obj):
        """Вывод дополнительной информации"""
        if int(obj.min_amount) >= int(obj.amount):
            return str('Необходимо докупить')
        else:
            return str('Докупать не требуется')


class StorageAdditionsSerializer(serializers.ModelSerializer):
    """Сериализатор склада дополнений"""
    message_additions = serializers.SerializerMethodField()

    class Meta:
        model = StorageAdditions
        fields = '__all__'

    def get_message_additions(self, obj):
        """Вывод дополнительной информации"""
        if int(obj.min_amount) >= int(obj.amount):
            return str('Необходимо докупить')
        else:
            return str('Докупать не требуется')


class IngredientsFoodSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов продуктов"""
    class Meta:
        model = IngredientsFood
        fields = '__all__'


class IngredientsAdditionsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов дополнений"""
    class Meta:
        model = IngredientsAdditions
        fields = '__all__'


class FilterCommentDecorSerializer(serializers.ListSerializer):
    """Вывод всех комментариев декоров без детей"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentDecorCildrenSerializer(serializers.ModelSerializer):
    """Вывод детей к комментарию декора"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

    class Meta:
        model = CommentDecor
        fields = ('author', 'content', 'created_at')


class CommentDecorSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев декора"""
    children = CommentDecorCildrenSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentDecorSerializer
        model = CommentDecor
        fields = ('author', 'content', 'created_at', 'children')


class DecorListSerializer(serializers.ModelSerializer):
    """Сериализатор декоров"""
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Decor
        fields = ('name', 'image', 'price', 'comments')

    def get_comments(self, obj):
        """Вывод последнего комментария"""
        comment = 'Комментариев нет'
        if obj.comments_decor.all():
            comment_list = [i for i in obj.comments_decor.all()]
            comment = str(comment_list[0].author) + '-' + str(comment_list[0].content)
        return comment


class DecorDetailSerializer(serializers.ModelSerializer):
    """Сериализатор декора"""
    cost_price_decor = serializers.SerializerMethodField()
    comments_decor = CommentDecorSerializer(many=True, read_only=True)

    class Meta:
        model = Decor
        exclude = ('is_active', )

    def get_cost_price_decor(self, obj):
        """Функция нахождения себестоимости декора"""
        price_food = 0
        price_add = 0
        if obj.ing_food:
            price_food = int(obj.ing_food.price)
        if obj.ing_add:
            price_add = int(obj.ing_add.price)
        return price_food + price_add


class OrdersSerializer(serializers.ModelSerializer):
    """Сериализатор заказов"""
    class Meta:
        model = Orders
        fields = '__all__'


class FilterCommentSerializer(serializers.ListSerializer):
    """Вывод всех комментариев десертов без детей"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentCildrenSerializer(serializers.ModelSerializer):
    """Вывод детей к комментарию десерта"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('author', 'content', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев десертов"""
    children = CommentCildrenSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ('author', 'content', 'created_at', 'children')


class DessertsListSerializer(serializers.ModelSerializer):
    """Сериализатор десертов"""
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Desserts
        fields = ('name', 'image', 'price', 'comments')

    def get_comments(self, obj):
        """Вывод последнего комментария"""
        comment = 'Комментариев нет'
        if obj.comments.all():
            comment_list = [i for i in obj.comments.all()]
            comment = str(comment_list[0].author) + '-' + str(comment_list[0].content)
        return comment


class DessertsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор десерта"""
    cost_price = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Desserts
        exclude = ('is_active', )

    def get_cost_price(self, obj):
        """Функция нахождения себестоимости десерта"""
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