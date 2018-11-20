from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


def get_user_file_path(user, filename):
    """
    Returns the path to the file for the specified user.

    :param user: user to look for
    :param filename: the filename
    :return: path to upload location
    """
    return 'users/{0}/{1}'.format(user.user.username, filename)


class Recipe(models.Model):
    """
    A user-uploaded recipe. Recipes can be created by registered users and are the core feature of the application.
    """
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField('Category')
    summary = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=get_user_file_path, default=None, blank=True, null=True)
    prep_time = models.CharField(max_length=200)
    cook_time = models.CharField(max_length=200)
    servings = models.IntegerField()
    calories = models.IntegerField()
    is_featured = models.BooleanField(default=False)

    def avg_rating(self):
        result = self.review_set.aggregate(Avg('rating'))['rating__avg']
        if result is None:
            return 0
        else:
            return result

    def user_can_review(self, user):
        has_reviewed = Review.objects.filter(user=user, recipe=self).count() > 0
        return (user.is_authenticated and not has_reviewed and self.user is not user) or user.is_superuser


class Ingredient(models.Model):
    """
    An ingredient in a user-submitted recipe. Each ingredient has a name entry, quantity, and index in the order of
    appearance in the recipe.
    """
    created_at = models.DateTimeField()
    ingredient = models.ForeignKey('IngredientName', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    index = models.IntegerField()


class Direction(models.Model):
    """
    A single direction for a recipe. Directions tell the user "how" to make the recipe. Each direction has a description
    text and index in the order of appearance.
    """
    created_at = models.DateTimeField()
    text = models.CharField(max_length=1000)
    index = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Category(models.Model):
    """
    A recipe category. Recipes may have multiple categories and categories can also have children categories. Not all
    categories can be assigned to recipes as marked by the __assignable__ field. This is so that categories can also
    serve as an empty container for children categories for browsing.
    """
    created_at = models.DateTimeField()
    name = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, default=None, blank=True)
    assignable = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name


class IngredientName(models.Model):
    """
    An ingredient name value. Normalized so that an ingredient's name is not simply a string but rather a row in the
    database. This is useful for browsing purpose.
    """
    created_at = models.DateTimeField()
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    A user-submitted review on a recipe. Every user can submit one review on each recipe that is not their own. Each
    review has a description and number rating between one and five.
    """
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.CharField(max_length=1000)
