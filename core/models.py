from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class Category(models.Model):
    created_at = models.DateTimeField()
    name = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, default=None, blank=True)
    assignable = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name


class Recipe(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    summary = models.CharField(max_length=1000)
    prep_time = models.CharField(max_length=200)
    cook_time = models.CharField(max_length=200)
    servings = models.IntegerField()
    calories = models.IntegerField()
    is_featured = models.BooleanField(default=False)

    def avg_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def is_trending(self):
        trending_cutoff = timezone.now() - timezone.timedelta(seconds=settings.TRENDING['time_window'])
        trending_count = self.review_set.filter(created_at__gt=trending_cutoff).count()
        return trending_count >= settings.TRENDING['review_count']


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


class Review(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.CharField(max_length=1000)
