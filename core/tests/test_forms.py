from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from core.forms import SubmitRecipeForm
from core.models import Category, IngredientName


class SubmitRecipeFormTestCase(TestCase):

    def setUp(self):
        Category.objects.create(
            created_at=timezone.now(),
            name='test_category_1',
            display_name='Test category 1',
            assignable=True
        )
        Category.objects.create(
            created_at=timezone.now(),
            name='test_category_2',
            display_name='Test category 2',
            assignable=False
        )
        User.objects.create(
            username='test_user_submit_recipe',
            email='test_user_submit_recipe@example.com',
            password='test_user_submit_recipe_password'
        )
        IngredientName.objects.create(created_at=timezone.now(), name='test_ing_1')

    def test_submit(self):
        post = self.post_data()
        form = SubmitRecipeForm(post)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.user = User.objects.get(username='test_user_submit_recipe')
        recipe.save()
        recipe.categories.set(form.cleaned_data['categories'])
        form.save_ingredients(recipe)
        form.save_directions(recipe)
        self.assertIsNotNone(recipe.categories.get(name='test_category_1'))
        self.assertIsNotNone(recipe.ingredient_set.get(ingredient__name='test_ing_1'))
        self.assertIsNotNone(recipe.ingredient_set.get(ingredient__name='test_ing_2'))
        self.assertIsNotNone(recipe.direction_set.get(index=1))
        self.assertIsNotNone(recipe.direction_set.get(index=2))

    def test_not_assignable_category(self):
        post = self.post_data()
        post['categories'].append(2)
        form = SubmitRecipeForm(post)
        self.assertFalse(form.is_valid())

    def test_missing_quantity(self):
        post = self.post_data()
        del post['quantity1']
        form = SubmitRecipeForm(post)
        self.assertFalse(form.is_valid())

    @staticmethod
    def post_data():
        return {
            'name': 'test_recipe',
            'summary': 'test summary 123',
            'servings': 20,
            'calories': 100,
            'categories': [1],
            'prep_time_num': 10,
            'prep_time_unit': 'minutes',
            'cook_time_num': 5,
            'cook_time_unit': 'minutes',
            'ing_name1': 'test_ing_1',
            'ing_name2': 'test_ing_2',
            'quantity1': 1,
            'quantity2': 2,
            'dir_text1': 'direction_1',
            'dir_text2': 'direction_2'
        }
