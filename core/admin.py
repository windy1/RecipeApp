from django.contrib import admin

from core import models


admin.site.register(models.Recipe)
admin.site.register(models.Ingredient)
admin.site.register(models.Direction)
admin.site.register(models.Category)
admin.site.register(models.IngredientName)
admin.site.register(models.Review)
admin.site.register(models.UserProfile)
