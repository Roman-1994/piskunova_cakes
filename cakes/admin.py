from django.contrib import admin
from cakes.models import *
from django.utils.safestring import mark_safe


class StorageFoodAdmin(admin.ModelAdmin):
    """Админка склада продуктов"""
    list_display = ('name', 'amount', 'min_amount', 'unit_measure', 'get_message_food')
    list_display_links = ('name',)
    list_editable = ('amount', 'min_amount')
    fields = ('name', 'amount', 'unit_measure', 'price', 'min_amount', 'get_message_food')
    search_fields = ('name', 'price')
    readonly_fields = ('get_message_food', )

    def get_message_food(self, obj):
        """Вывод дополнительной информации"""
        if int(obj.min_amount) >= int(obj.amount):
            return str('Необходимо докупить')
        else:
            return str('Докупать не требуется')

    get_message_food.short_description = 'Дополнительная информация'


class StorageAdditionsAdmin(admin.ModelAdmin):
    """Админка склада дополнений"""
    list_display = ('name', 'amount', 'min_amount', 'unit_measure', 'get_message_additions')
    list_display_links = ('name',)
    list_editable = ('amount', 'min_amount')
    fields = ('name', 'amount', 'unit_measure', 'price', 'min_amount', 'get_message_additions')
    search_fields = ('name', 'price')
    readonly_fields = ('get_message_additions', )

    def get_message_additions(self, obj):
        """Вывод дополнительной информации"""
        if int(obj.min_amount) >= int(obj.amount):
            return str('Необходимо докупить')
        else:
            return str('Докупать не требуется')

    get_message_additions.short_description = 'Дополнительная информация'


class AdditionalImageAdmin(admin.TabularInline):
    """Дополнительные изображения к админкам декоров и десертов"""
    model = AdditionalImage
    fields = ('image', )
    extra = 2


class CommentInlineAdmin(admin.TabularInline):
    """Дополнение комментариев к админке десертов"""
    model = Comment
    extra = 1


class PriceDessertsListFilter(admin.SimpleListFilter):
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('super_low', 'до 1000 рублей'),
            ('low', 'до 2000 рублей'),
            ('medium', 'до 3000 рублей'),
            ('high', 'до 5000 рублей'),
            ('super_high', 'свыше 5000 рублей')
        )

    def queryset(self, request, queryset):
        if self.value() == 'super_low':
            return queryset.filter(price__lt=1000)
        elif self.value() == 'low':
            return queryset.filter(price__gte=1000, price__lt=2000)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=2000, price__lt=3000)
        elif self.value() == 'high':
            return queryset.filter(price__gte=3000, price__lt=5000)
        elif self.value() == 'super_high':
            return queryset.filter(price__gte=5000)


class DessertsAdmin(admin.ModelAdmin):
    """Админка десертов"""
    list_display = ('name', 'amount', 'weight', 'price', 'get_cost_price', 'get_revenue_desserts', 'get_html_photo')
    fields = ('name', 'decor', 'amount', 'weight', ('price', 'get_cost_price', 'get_revenue_desserts'), 'ing_food', 'ing_add', ('image', 'get_html_photo'), 'is_active', 'created_at')
    inlines = (AdditionalImageAdmin, CommentInlineAdmin)
    readonly_fields = ('get_cost_price', 'get_revenue_desserts', 'get_html_photo')
    search_fields = ('name', 'decor__name', 'price')
    list_filter = ('decor__name', 'amount', 'weight', PriceDessertsListFilter)
    save_on_top = True

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

    def get_revenue_desserts(self, obj):
        """Нахождение выручки"""
        return obj.price - self.get_cost_price(obj)

    def get_html_photo(self, obj):
        """Вывод фото, а не URL"""
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")

    get_cost_price.short_description = 'Себестоимость'
    get_revenue_desserts.short_description = 'Выручка'
    get_html_photo.short_description = 'Миниатюра'


class CommentDecorInlineAdmin(admin.TabularInline):
    """Дополнение комментариев к админке декоров"""
    model = CommentDecor
    extra = 1


class PriceDecorsListFilter(admin.SimpleListFilter):
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'до 500 рублей'),
            ('medium', 'до 1000 рублей'),
            ('high', 'свыше 1000 рублей'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=500, price__lt=1000)
        elif self.value() == 'high':
            return queryset.filter(price__gte=1000)


class DecorAdmin(admin.ModelAdmin):
    """Админка декоров"""
    list_display = ('name', 'price', 'get_cost_price_decor', 'get_revenue_decors', 'get_html_photo')
    fields = ('name', ('price', 'get_cost_price_decor', 'get_revenue_decors'), 'ing_food', 'ing_add', 'image', 'is_active', 'created_at')
    inlines = (AdditionalImageAdmin,  CommentDecorInlineAdmin)
    readonly_fields = ('get_cost_price_decor', 'get_revenue_decors', 'get_html_photo')
    search_fields = ('name', 'price')
    list_filter = (PriceDecorsListFilter, )
    save_on_top = True

    def get_cost_price_decor(self, obj):
        """Функция нахождения себестоимости декора"""
        price_food = 0
        price_add = 0
        if obj.ing_food:
            price_food = int(obj.ing_food.price)
        if obj.ing_add:
            price_add = int(obj.ing_add.price)
        return price_food + price_add

    def get_revenue_decors(self, obj):
        """Нахождение выручки"""
        return obj.price - self.get_cost_price_decor(obj)

    def get_html_photo(self, obj):
        """Вывод фото, а не URL"""
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")

    get_cost_price_decor.short_description = 'Себестоимость'
    get_revenue_decors.short_description = 'Выручка'
    get_html_photo.short_description = 'Миниатюра'


class IngredientsFoodAdmin(admin.ModelAdmin):
    """Админка ингредиетов продуктов"""
    list_display = ('name_food', 'amount', 'unit_measure', 'price')
    fields = ('name_food', 'amount', 'unit_measure', 'price')


class IngredientsAdditionsAdmin(admin.ModelAdmin):
    """Админка ингредиетов дополнений"""
    list_display = ('name_addition', 'amount', 'unit_measure', 'price')
    fields = ('name_food', 'amount', 'unit_measure', 'price')


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('dessert', 'filling', 'get_html_photo')
    fields = ('dessert', 'filling', ('img_decor', 'get_html_photo'), 'add_wishes', 'customer', 'phone', 'self_service', 'delivery', 'datetime_delivery', 'created_at')
    readonly_fields = ('get_html_photo', )

    def get_html_photo(self, obj):
        if obj.img_decor:
            return mark_safe(f"<img src='{obj.img_decor.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'


class CommentAdmin(admin.ModelAdmin):
    """Админка комментариев десертов"""
    list_display = ('dessert', 'parent', 'author', 'created_at')
    fields = ('dessert', 'parent', 'author', 'content', 'is_active')


class CommentDecorAdmin(admin.ModelAdmin):
    """Админка комментариев декоров"""
    list_display = ('decor', 'parent', 'author', 'created_at')
    fields = ('decor', 'parent', 'author', 'content', 'is_active')


class RatingAdmin(admin.ModelAdmin):
    """Админка рейтинга"""
    list_display = ('__str__', )
    fields = ('ip', 'star', 'dessert')


def get_cost_price(obj):
    """Функция нахождения себестоимости десерта для ProfitAdmin"""
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


class ProfitAdmin(admin.ModelAdmin):
    """Админка прибыли"""
    list_display = ('start_period', 'end_period', 'get_profit')
    fields = ('start_period', 'end_period')

    def get_profit(self, obj):
        list_desserts = Desserts.objects.filter(created_at__date__gte=obj.start_period, created_at__date__lte=obj.end_period)  #created_at__year__gte=obj.start_period, created_at__year__lte=obj.end_period
        res = []
        for i in list_desserts:
            res.append(i.price - get_cost_price(i))
        return sum(res)

    get_profit.short_description = 'Прибыль за период'


admin.site.register(StorageFood, StorageFoodAdmin)
admin.site.register(StorageAdditions, StorageAdditionsAdmin)
admin.site.register(Desserts, DessertsAdmin)
admin.site.register(Decor, DecorAdmin)
admin.site.register(IngredientsFood, IngredientsFoodAdmin)
admin.site.register(IngredientsAdditions, IngredientsAdditionsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentDecor, CommentDecorAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Profit, ProfitAdmin)
