from django.contrib import admin

from .models import Recipe, Ingredient, Direction, Category, IngredientName, Review


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Direction)
admin.site.register(Category)
admin.site.register(IngredientName)
admin.site.register(Review)
