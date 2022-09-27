from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class StorageFood(models.Model):
    """Mодель склада продуктов"""
    name = models.CharField(max_length=50, verbose_name='Наименование')
    amount = models.IntegerField(verbose_name='Количество')
    unit_measure = models.CharField(max_length=10, verbose_name='Единица измерения')
    price = models.IntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад продуктов'
        ordering = ('name',)


class StorageAdditions(models.Model):
    """модель склада дополнений"""
    name = models.CharField(max_length=50, verbose_name='Наименование')
    amount = models.IntegerField(verbose_name='Количество')
    unit_measure = models.CharField(max_length=10, verbose_name='Единица измерения')
    price = models.IntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад дополнений'
        ordering = ('name',)


class IngredientsFood(models.Model):
    """Ингредиенты продуктов"""
    name_food = models.ForeignKey(StorageFood, on_delete=models.CASCADE, related_name='indredietsfood',
                                  verbose_name='Наименование продукта', blank=True, null=True)
    amount = models.IntegerField(verbose_name='Количество')
    unit_measure = models.CharField(max_length=10, verbose_name='Единица измерения')
    price = models.IntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return '%s - %s' % (self.name_food, self.amount)

    class Meta:
        verbose_name = 'Ингредиенты продуктов'
        ordering = ('name_food',)


class IngredientsAdditions(models.Model):
    """Ингредиенты дополнений"""
    name_addition = models.ForeignKey(StorageAdditions, on_delete=models.CASCADE, related_name='indredietsadditions',
                                  verbose_name='Наименование дополнения', blank=True, null=True)
    amount = models.IntegerField(verbose_name='Количество')
    unit_measure = models.CharField(max_length=10, verbose_name='Единица измерения')
    price = models.IntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return '%s - %s' % (self.name_addition, self.amount)

    class Meta:
        verbose_name = 'Ингредиенты дополнений'
        ordering = ('name_addition',)


class Decor(models.Model):
    """Декор"""
    name = models.CharField(max_length=50, verbose_name='Наименование')
    ing_food = models.ForeignKey(IngredientsFood, on_delete=models.CASCADE, verbose_name='Ингредиенты продуктов', blank=True, null=True)
    ing_add = models.ForeignKey(IngredientsAdditions, on_delete=models.CASCADE, verbose_name='Список дополнений', blank=True, null=True)
    price = models.IntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декоры'
        ordering = ('name', 'price')


class Desserts(models.Model):
    """Десерты"""
    name = models.CharField(max_length=50, verbose_name='Название')
    decor = models.ForeignKey(Decor, on_delete=models.DO_NOTHING, verbose_name='Декор', blank=True, null=True)
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')
    weight = models.FloatField(default=0, verbose_name='Вес')
    price = models.FloatField(default=0, verbose_name='Цена')
    ing_food = models.ManyToManyField(IngredientsFood, related_name='ing_food', verbose_name='Ингредиенты продуктов')
    ing_add = models.ManyToManyField(IngredientsAdditions, related_name='ing_addinion', verbose_name='Список дополнений')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Десерт'
        verbose_name_plural = 'Десерты'
        ordering = ('name', 'price')


class Orders(models.Model):
    """Заказы"""
    dessert = models.ForeignKey(Desserts, on_delete=models.PROTECT, verbose_name='Наменование')
    add_wishes = models.TextField(max_length=5000, verbose_name='Дополнительные пожелания')
    сustomer = models.ForeignKey(User, on_delete=models.SET('Заказчик'), verbose_name='Заказчик')
    phone = models.CharField(max_length=11, default='-', verbose_name='Телефон')
    self_service = models.BooleanField(default=False, verbose_name='Самовывоз', help_text='Адрес смотрите в разделе контакты')
    delivery = models.TextField(max_length=500, verbose_name='Адрес доставки', help_text='Если вы выбрали сомовывоз, напишите в этом окне время когда вы приедете за заказом')
