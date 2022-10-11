from django.contrib import admin
from cakes.models import *


class StorageFoodAdmin(admin.ModelAdmin):
    """Админка склада продуктов"""
    list_display = ('name', 'amount', 'unit_measure')
    fields = ('name', 'amount', 'unit_measure', 'price', 'min_amount')


class StorageAdditionsAdmin(admin.ModelAdmin):
    """Админка склада дополнений"""
    list_display = ('name', 'amount', 'unit_measure')
    fields = ('name', 'amount', 'unit_measure', 'price', 'min_amount')


class AdditionalImageAdmin(admin.TabularInline):
    """Дополнительные изображения к админкам декоров и десертов"""
    model = AdditionalImage
    extra = 2


class CommentInlineAdmin(admin.TabularInline):
    """Дополнение комментариев к админке десертов"""
    model = Comment
    extra = 1


class DessertsAdmin(admin.ModelAdmin):
    """Админка десертов"""
    list_display = ('name', 'amount', 'weight', 'price')
    fields = ('name', 'decor', 'amount', 'weight', 'price', 'ing_food', 'ing_add', 'image', 'is_active', 'created_at')
    inlines = (AdditionalImageAdmin, CommentInlineAdmin)


class CommentDecorInlineAdmin(admin.TabularInline):
    """Дополнение комментариев к админке декоров"""
    model = CommentDecor
    extra = 1


class DecorAdmin(admin.ModelAdmin):
    """Админка декоров"""
    list_display = ('name', 'price')
    fields = ('name', 'price', 'ing_food', 'ing_add', 'image', 'is_active', 'created_at')
    inlines = (AdditionalImageAdmin,  CommentDecorInlineAdmin)


class IngredientsFoodAdmin(admin.ModelAdmin):
    """Админка ингредиетов продуктов"""
    list_display = ('name_food', 'amount', 'unit_measure', 'price')


class IngredientsAdditionsAdmin(admin.ModelAdmin):
    """Админка ингредиетов дополнений"""
    list_display = ('name_addition', 'amount', 'unit_measure', 'price')


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('dessert', 'filling', 'img_decor')
    fields = ('dessert', 'filling', 'img_decor', 'add_wishes', 'customer', 'phone', 'self_service', 'delivery', 'datetime_delivery', 'created_at')


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
