from django.contrib import admin

from .models import *


admin.site.register(Recipe)
admin.site.register(IngredientName)
admin.site.register(Ingredient)
admin.site.register(Direction)
admin.site.register(Review)
admin.site.register(Category)
