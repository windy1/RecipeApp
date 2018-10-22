from django.contrib import admin

from .models import Recipe, IngredientName, Ingredient, Direction


admin.site.register(Recipe)
admin.site.register(IngredientName)
admin.site.register(Ingredient)
admin.site.register(Direction)
