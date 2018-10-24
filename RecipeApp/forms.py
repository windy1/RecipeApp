from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.conf import settings

from .models import *


class SignUpForm(UserCreationForm):
    """
    See: registration/signUp.html template
    """
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class IngredientData:
    def __init__(self, quantity=None, name=None):
        self.quantity = quantity
        self.name = name


class SubmitRecipeForm(forms.ModelForm):

    def is_valid(self):
        # force a clean of the form
        self.full_clean()
        return super().is_valid()

    def clean(self):
        # TODO: more validation?
        self._cleanIngredients()
        self._cleanDirections()
        return super().clean()

    def _cleanIngredients(self):
        """
        Collect all the ingredient data submitted and verify that it is valid.
        """
        ingredients = {}
        ingNum = 1
        nameField = 'ingName%d' % ingNum
        # While there is a numbered ingredient name value
        while self.data.get(nameField):
            ingName = self.data[nameField]
            quantityField = 'quantity%d' % ingNum

            self.fields[nameField] = forms.CharField()
            self.fields[quantityField] = forms.IntegerField()

            quantityVal = self.data.get(quantityField)
            if not quantityVal:
                raise forms.ValidationError(
                    'Missing quantity for ingredient: %(name)',
                    params={'name': ingName},
                    code='missing_quantity'
                )
            elif int(quantityVal) < 1:
                raise forms.ValidationError(
                    'Invalid value for quantity.',
                    code='invalid_quantity'
                )
            elif IngredientName.objects.filter(name=ingName).count() == 0:
                self.add_error(nameField, 'No such ingredient %s exists' % ingName)
            else:
                ingredients[ingNum] = IngredientData(name=ingName, quantity=self.data[quantityField])

            ingNum += 1
            nameField = 'ingName%d' % ingNum

        self.cleaned_data['ingredients'] = ingredients

    def _cleanDirections(self):
        """
        Collect all the direction data submitted and verify that it is valid.
        """
        directions = {}
        dirNum = 1
        textField = 'dirText%d' % dirNum
        while self.data.get(textField):
            dirText = self.data[textField]
            self.fields[textField] = forms.CharField()

            if len(dirText) > 1000:
                raise forms.ValidationError(
                    'Directions cannot be larger than 1000 characters.',
                    code='invalid_direction'
                )

            directions[dirNum] = dirText
            dirNum += 1
            textField = 'dirText%d' % dirNum

        self.cleaned_data['directions'] = directions

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.created_at = timezone.now()
        if commit:
            recipe.save()
        return recipe

    def createIngredients(self, recipe):
        """
        Creates the ingredients submitted in the form. New Recipe must be saved in database before this is called.

        :param recipe: recipe of ingredients
        """
        ingredients = self.cleaned_data['ingredients']
        for ingNum in ingredients:
            ing = ingredients[ingNum]
            Ingredient.objects.create(
                created_at=timezone.now(),
                ingredient=IngredientName.objects.get(name=ing.name),
                quantity=ing.quantity,
                recipe=recipe,
                index=ingNum)

    def createDirections(self, recipe):
        """
        Creates the directions submitted in the form. New Recipe must be saved in database before this is called.

        :param recipe: recipe of directions
        """
        directions = self.cleaned_data['directions']
        for dirNum in directions:
            Direction.objects.create(
                created_at=timezone.now(),
                text=directions[dirNum],
                index=dirNum,
                recipe=recipe)

    class Meta:
        model = Recipe
        fields = ('name', 'summary', 'prepTime', 'cookTime', 'servings', 'calories')


class ReviewRecipeForm(forms.ModelForm):

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and rating < settings.REVIEWS['rating_min'] or rating > settings.REVIEWS['rating_max']:
            raise forms.ValidationError('The rating is out of bounds.', code='invalid_rating')
        return rating

    class Meta:
        model = Review
        fields = ('rating', 'text')
