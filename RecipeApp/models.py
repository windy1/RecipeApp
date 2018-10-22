from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=1000)
    prepTime = models.CharField(max_length=200)
    cookTime = models.CharField(max_length=200)
    servings = models.IntegerField()
    calories = models.IntegerField()


class IngredientName(models.Model):
    created_at = models.DateTimeField()
    name = models.CharField(max_length=200, unique=True)


class Ingredient(models.Model):
    created_at = models.DateTimeField()
    ingredient = models.ForeignKey(IngredientName, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    index = models.IntegerField()


class Direction(models.Model):
    created_at = models.DateTimeField()
    text = models.CharField(max_length=1000)
    index = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
