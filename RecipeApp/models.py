from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=1000)
    # prepTime = models.TimeField()
    # cookTime = models.TimeField()
    servings = models.IntegerField()
    calories = models.IntegerField()
