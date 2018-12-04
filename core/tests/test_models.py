from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from core.models import Recipe, Category, Review


class RecipeTestCase(TestCase):
    """
    A test case for the functionality of the Recipe model.
    """

    def setUp(self):
        user = User.objects.create(username='test_user')
        cat = Category.objects.create(
            created_at=timezone.now(),
            name='test_category',
            display_name='Test categories',
            assignable=True
        )
        recipe = Recipe.objects.create(
            created_at=timezone.now(),
            user=user,
            name='test_recipe',
            summary='test_recipe_summary',
            prep_time='1 hour',
            cook_time='1 hour',
            servings=1,
            calories=1
        )
        recipe.categories.set([cat])
        Review.objects.create(created_at=timezone.now(), user=user, recipe=recipe, rating=5, text='review_1_text')
        Review.objects.create(created_at=timezone.now(), user=user, recipe=recipe, rating=0, text='review_2_text')

    def test_avg_rating(self):
        """
        Tests the aggregate function avg_rating in the Recipe model.
        """
        recipe = Recipe.objects.get(name='test_recipe')
        self.assertEqual(recipe.avg_rating(), 2.5)
