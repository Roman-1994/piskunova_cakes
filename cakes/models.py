from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class StorageFood(models.Model):
    """Mодель склада продуктов"""
    name = models.CharField(max_length=50, verbose_name='Наименование')
    amount = models.IntegerField(verbose_name='Количество')
    unit_measure = models.CharField(max_length=10, verbose_name='Единица измерения')
    price = models.IntegerField(default=0, verbose_name='Цена')
    min_amount = models.IntegerField(default=0, verbose_name='Минимально необходимое количество')

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
    min_amount = models.IntegerField(default=0, verbose_name='Минимально необходимое количество')

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
        """Метакласс модели ингредиенты дополнений"""
        verbose_name = 'Ингредиенты дополнений'
        ordering = ('name_addition',)


class Decor(models.Model):
    """Декор"""
    name = models.CharField(max_length=50, verbose_name='Наименование')
    ing_food = models.ForeignKey(IngredientsFood, on_delete=models.CASCADE, related_name='ing_decor_food', verbose_name='Ингредиенты продуктов', blank=True, null=True)
    ing_add = models.ForeignKey(IngredientsAdditions, on_delete=models.CASCADE, related_name='ing_decor_add', verbose_name='Список дополнений', blank=True, null=True)
    price = models.IntegerField(default=0, verbose_name='Цена')
    image = models.ImageField(blank=True, upload_to='media/decors/', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(db_index=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Функция удаления всех дополнительных изображений, при удалении записи в первичной модели"""
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Вычитание из склада продуктов и дополнений ингредиентов"""
        self.ing_food.name_food.amount -= self.ing_food.amount
        self.ing_food.name_food.save()
        self.ing_add.name_addition.amount -= self.ing_add.amount
        self.ing_add.name_addition.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декоры'
        ordering = ('-created_at', 'name', 'price')


class Desserts(models.Model):
    """Десерты"""
    name = models.CharField(max_length=50, verbose_name='Название')
    decor = models.ForeignKey(Decor, on_delete=models.DO_NOTHING, related_name='des_decor', verbose_name='Декор', blank=True, null=True)
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')
    weight = models.FloatField(default=0, verbose_name='Вес')
    price = models.FloatField(default=0, verbose_name='Цена')
    ing_food = models.ManyToManyField(IngredientsFood, related_name='ing_food', verbose_name='Ингредиенты продуктов')
    ing_add = models.ManyToManyField(IngredientsAdditions, related_name='ing_addinion', verbose_name='Список дополнений')
    image = models.ImageField(blank=True, upload_to='media/desserts/', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(db_index=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Функция удаления всех дополнительных изображений, при удалении записи в первичной модели"""
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Вычитание из склада продуктов и дополнений ингредиентов"""
        for f in self.ing_food.all():
            f.name_food.amount -= f.amount
            f.name_food.save()
        for a in self.ing_add.all():
            a.name_addition.amount -= a.amount
            a.name_addition.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Десерт'
        verbose_name_plural = 'Десерты'
        ordering = ('-created_at', 'name', 'price')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('desserts_detail', kwargs={'pk': self.pk})


class AdditionalImage(models.Model):
    """Модель дополнительных изображений"""
    dessert = models.ForeignKey(Desserts, on_delete=models.CASCADE, verbose_name='Десерт', related_name='add_img_des', blank=True, null=True)
    decor = models.ForeignKey(Decor, on_delete=models.CASCADE, verbose_name='Декор', related_name='add_img_dec', blank=True, null=True)
    image = models.ImageField(upload_to='media/add_img/', verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Orders(models.Model):
    """Заказы"""
    DESSERTS = (
        (None, 'Выберите десерт'),
        ('Торт', (
            ('Pie_1,5_kg', 'Торт - 1,5 кг'),
            ('Pie_2_kg', 'Торт - 2 кг'),
            ('Pie_2,5_kg', 'Торт - 2,5 кг'),
            ('Pie_3_kg', 'Торт - 3 кг'),
            ('Pie_3,5_kg', 'Торт - 3,5 кг'),
            ('Pie_4_kg', 'Торт - 4 кг'),
            ('Pie_4,5_kg', 'Торт - 4,5 кг'),
            ('Pie_5_kg', 'Торт - 5 кг'),
            ('Pie_5,5_kg', 'Торт - 5,5 кг'),
            ('Pie_6_kg', 'Торт - 6 кг'),
        )),
        ('Бенто торт', (
            ('Bento_рie_550_gr', 'Бенто торт - ~550 гр'),
            ('Big_bento_pie_800_gr', 'BIG бенто торт - ~800 гр'),
        )),
        ('Капкейки', (
            ('Cupcakes_6_grand_650_gr', 'Капкейки(6 шт.) - ~650 гр'),
            ('Cupcakes_9_grand_950_gr', 'Капкейки(9 шт.) - ~950 гр'),
            ('Cupcakes_12_grand_1300_gr', 'Капкейки(12 шт.) - ~1300 гр'),
        )),
        ('Трайфлы', (
            ('Trifles_4_grand_800_gr', 'Капкейки(4 шт.) - ~800 гр'),
            ('Trifles_6_grand_1200_gr', 'Капкейки(6 шт.) - ~1200 гр'),
            ('Trifles_9_grand_1800_gr', 'Капкейки(9 шт.) - ~1800 гр'),
            ('Trifles_12_grand_2400_gr', 'Капкейки(12 шт.) - ~2400 гр'),
        )),
        ('Кейк попсы в виде сердца', (
            ('Cake_pop_heart_4_grand_600_gr', 'Кейк попсы(4 шт.) - ~600 гр'),
            ('Cake_pop_heart_6_grand_900_gr', 'Кейк попсы(6 шт.) - ~900 гр'),
            ('Cake_pop_heart_9_grand_1350_gr', 'Кейк попсы(9 шт.) - ~1350 гр'),
            ('Cake_pop_heart_12_grand_1800_gr', 'Кейк попсы(12 шт.) - ~1800 гр'),
        )),
        ('Набор (бенто торт или BIG бенто торт + капкейки (5 шт.) или трайфлы (5 шт.))', (
            ('Bento_рie + cupcakes', 'Бенто торт + капкейки'),
            ('Bento_рie + trifles', 'Бенто торт + трайфлы'),
            ('Big_bento_pie + cupcakes', 'BIG бенто торт + капкейки'),
            ('Big_bento_pie + trifles', 'BIG бенто торт + трайфлы'),
        )),
    )

    FILLING = (
        (None, 'Выберите начинку'),
        ('Raspberry', 'Малина'),
        ('Cherry', 'Вишня'),
        ('Snickers', 'Сникерс'),
    )

    dessert = models.CharField(max_length=50, choices=DESSERTS, verbose_name='Наменование', default='Выберите десерт')
    filling = models.CharField(max_length=50, choices=FILLING, verbose_name='Начинка', default='Выберите начинку')
    img_decor = models.ImageField(upload_to='orders', verbose_name='Изображение декора', default='-')
    add_wishes = models.TextField(max_length=5000, verbose_name='Дополнительные пожелания', blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET('Заказчик'), verbose_name='Заказчик')
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    self_service = models.BooleanField(default=False, verbose_name='Самовывоз?', help_text='Адрес кондитера смотрите в разделе контакты')
    delivery = models.TextField(max_length=500, verbose_name='Адрес доставки', blank=True, null=True, help_text='Данное поле заполняется только если вам нужна доставка, а не самовывоз')
    datetime_delivery = models.DateTimeField(db_index=True, verbose_name='Дата и время доставки или самовывоза', blank=True, null=True)
    created_at = models.DateTimeField(db_index=True, verbose_name='Дата заказа', default=datetime.today)

    def __str__(self):
        return '%s - %s' % (self.dessert, self.filling)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)


class Comment(models.Model):
    """Модель комментариев десертов"""
    dessert = models.ForeignKey(Desserts, on_delete=models.CASCADE, verbose_name='Десерт', related_name='comments')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    author = models.CharField(max_length=50, verbose_name='Автор')
    content = models.TextField(max_length=1000, verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')

    def __str__(self):
        return '%s - %s' % (self.dessert, self.author)

    class Meta:
        verbose_name = 'Комментарий десерта'
        verbose_name_plural = 'Комментарии десертов'
        ordering = ('dessert', '-created_at')


class CommentDecor(models.Model):
    """Модель комментариев декоров"""
    decor = models.ForeignKey(Decor, on_delete=models.CASCADE, verbose_name='Декор', related_name='comments_decor')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    author = models.CharField(max_length=50, verbose_name='Автор')
    content = models.TextField(max_length=1000, verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')

    def __str__(self):
        return '%s - %s' % (self.decor, self.author)

    class Meta:
        verbose_name = 'Комментарий декора'
        verbose_name_plural = 'Комментарии декоров'
        ordering = ('decor', '-created_at')


class Rating(models.Model):
    """Модель рейтинга"""
    STAR = (
        (None, 'Выберите рейтинг'),
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    ip = models.CharField('IP адрес', max_length=15)
    star = models.IntegerField(choices=STAR, verbose_name='Звезда')
    dessert = models.ForeignKey('Desserts', on_delete=models.CASCADE, verbose_name='Десерт')

    def __str__(self):
        return f'{self.star} - {self.dessert}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Profit(models.Model):
    """Модель прибыли"""
    start_period = models.DateField(default=datetime.today, verbose_name='Начало периода')
    end_period = models.DateField(default=datetime.today, verbose_name='Конец периода')

    class Meta:
        verbose_name = 'Прибыль'
        verbose_name_plural = 'Прибыли'

