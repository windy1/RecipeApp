from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


def user_directory_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.user.username, filename)


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
    image = models.ImageField(upload_to=user_directory_path, default=None, blank=True, null=True)
    prep_time = models.CharField(max_length=200)
    cook_time = models.CharField(max_length=200)
    servings = models.IntegerField()
    calories = models.IntegerField()
    is_featured = models.BooleanField(default=False)

    def avg_rating(self):
        result = self.review_set.aggregate(Avg('rating'))['rating__avg']
        if result is None:
            return 3
        else:
            return result


class IngredientName(models.Model):
    created_at = models.DateTimeField()
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


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
