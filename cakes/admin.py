from django.contrib import admin
from cakes.models import *


class StorageFoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'unit_measure')
    fields = ('name', 'amount', 'unit_measure')


class StorageAdditionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'unit_measure')
    fields = ('name', 'amount', 'unit_measure')


class DessertsAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'weight', 'price')
    fields = ('name', 'decor', 'amount', 'weight', 'price', 'ing_food', 'ing_add')


class DecorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = ('name', 'price', 'ing_food', 'ing_add')


class IngredientsFoodAdmin(admin.ModelAdmin):
    list_display = ('name_food', 'amount', 'unit_measure', 'price')


class IngredientsAdditionsAdmin(admin.ModelAdmin):
    list_display = ('name_addition', 'amount', 'unit_measure', 'price')


admin.site.register(StorageFood, StorageFoodAdmin)
admin.site.register(StorageAdditions, StorageAdditionsAdmin)
admin.site.register(Desserts, DessertsAdmin)
admin.site.register(Decor, DecorAdmin)
admin.site.register(IngredientsFood, IngredientsFoodAdmin)
admin.site.register(IngredientsAdditions, IngredientsAdditionsAdmin)

