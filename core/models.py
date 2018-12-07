from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.utils import timezone


def user_file_path(user, filename):
    """
    Returns the path to the file for the specified users.

    :param user: users to look for
    :param filename: the filename
    :return: path to upload location
    """
    return 'users/{0}/{1}'.format(user.user.username, filename)


class Recipe(models.Model):
    """
    A users-uploaded recipes. Recipes can be created by registered users and are the core feature of the application.
    """
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField('Category')
    summary = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=user_file_path, default=None, blank=True, null=True)
    prep_time = models.CharField(max_length=200)
    cook_time = models.CharField(max_length=200)
    servings = models.IntegerField()
    calories = models.IntegerField()
    is_featured = models.BooleanField(default=False)

    def avg_rating(self):
        """
        Returns the average rating of this recipe based on all reviews submitted by users.

        :return: average rating
        """
        result = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return result if result else 0

    def avg_percent_rating(self):
        return str(self.avg_rating() * 30) + '%'

    def avg_percent_rating_large(self):
        return str(self.avg_rating() * 50) + '%'

    def user_can_review(self, user):
        """
        Returns true if the specified user is permitted to review this recipe.

        :param user: to check permission of
        :return: true if user can review the recipe
        """
        return (user.is_authenticated
                and Review.objects.filter(user=user, recipe=self).count() == 0
                and self.user is not user) or user.is_superuser

    def __str__(self):
        return '%s by %s' % (self.name, self.user.username)


class Ingredient(models.Model):
    """
    An ingredient in a users-submitted recipes. Each ingredient has a name entry, quantity, and index in the order of
    appearance in the recipes.
    """
    created_at = models.DateTimeField()
    ingredient = models.ForeignKey('IngredientName', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    index = models.IntegerField()


class Direction(models.Model):
    """
    A single direction for a recipes. Directions tell the users "how" to make the recipes. Each direction has a
    description text and index in the order of appearance.
    """
    created_at = models.DateTimeField()
    text = models.CharField(max_length=1000)
    index = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Category(models.Model):
    """
    A recipes categories. Recipes may have multiple categories and categories can also have children categories. Not all
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
    A users-submitted review on a recipes. Every users can submit one review on each recipes that is not their own. Each
    review has a description and number rating between one and five.
    """
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.CharField(max_length=1000)

    def __str__(self):
        return 'Review for recipes #%d by %s' % (self.recipe.id, self.user.username)


class UserProfile(models.Model):
    """
    User profile data that is displayed on the assoiated user's profile page.
    """
    created_at = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to=user_file_path, default=None, blank=True, null=True)
    bio = models.CharField(max_length=1000, default=None, blank=True, null=True)

    @staticmethod
    def get_or_create(user):
        return UserProfile.objects.get_or_create(user=user, defaults={'created_at': timezone.now()})

    def __str__(self):
        return 'User profile for %s' % self.user.username
