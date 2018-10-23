from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.conf import settings

from .models import *


class SignUpForm(UserCreationForm):
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
        self.full_clean()
        return super().is_valid()

    def clean(self):
        # TODO: more validation
        self._cleanIngredients()
        self._cleanDirections()
        return super().clean()

    def _cleanIngredients(self):
        ingredients = {}
        ingNum = 1
        nameField = 'ingName%d' % ingNum
        while self.data.get(nameField):
            ingName = self.data[nameField]
            quantityField = 'quantity%d' % ingNum

            self.fields[nameField] = forms.CharField()
            self.fields[quantityField] = forms.CharField()

            if not self.data.get(quantityField):
                self.add_error(quantityField, 'Missing quantity for ingredient: %s' % ingName)
            elif IngredientName.objects.filter(name=ingName).count() == 0:
                self.add_error(nameField, 'No such ingredient %s exists' % ingName)
            else:
                ingredients[ingNum] = IngredientData(name=ingName, quantity=self.data[quantityField])

            ingNum += 1
            nameField = 'ingName%d' % ingNum

        self.cleaned_data['ingredients'] = ingredients

    def _cleanDirections(self):
        directions = {}
        dirNum = 1
        textField = 'dirText%d' % dirNum
        while self.data.get(textField):
            dirText = self.data[textField]
            self.fields[textField] = forms.CharField()
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
    class Meta:
        model = Review
        fields = ('rating', 'text')

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and rating < settings.REVIEWS['rating_min'] or rating > settings.REVIEWS['rating_max']:
            raise forms.ValidationError('The rating is out of bounds.', code='invalid_rating')
        return rating
