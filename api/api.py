from rest_framework import serializers
from django.contrib.auth.models import User

from core.models import Recipe, Category, Ingredient, Review, IngredientName


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'date_joined', 'recipe_set')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    directions = serializers.SerializerMethodField()

    @staticmethod
    def get_ingredients(model):
        res = []
        for ing in model.ingredient_set.all():
            res.append({'name': ing.ingredient.name, 'quantity': ing.quantity, 'index': ing.index})
        return res

    @staticmethod
    def get_directions(model):
        res = []
        for direction in model.direction_set.all():
            res.append({'text': direction.text, 'index': direction.index})
        return res

    class Meta:
        model = Recipe
        fields = (
            'created_at', 'users', 'name', 'categories', 'summary', 'prep_time', 'cook_time', 'servings', 'calories',
            'is_featured', 'review_count', 'avg_rating', 'categories', 'ingredients', 'directions', 'review_set'
        )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('created_at', 'name', 'parent', 'assignable')


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('quantity', 'index')


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ('created_at', 'users', 'recipes', 'rating', 'text')


class IngredientNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IngredientName
        fields = ('created_at', 'name')
