from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class SignUpForm(UserCreationForm):
    """
    See: registration/signup.html template
    """
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class IngredientData:
    def __init__(self, quantity=None, name=None):
        self.quantity = quantity
        self.name = name


class SubmitRecipeForm(forms.ModelForm):

    time_units = [('minutes', 'minutes'), ('hours', 'hours'), ('days', 'days')]

    prep_time_num = forms.IntegerField(min_value=1, max_value=60)
    prep_time_unit = forms.ChoiceField(choices=time_units)
    cook_time_num = forms.IntegerField(min_value=1, max_value=60)
    cook_time_unit = forms.ChoiceField(choices=time_units)

    def __init__(self, post=None, files=None):
        super().__init__(data=post, files=files)
        self.fields['prep_time_unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['cook_time_unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['categories'].queryset = Category.objects.filter(assignable=True)
        self.fields['categories'].widget.attrs.update({
            'class': 'form-control',
            'aria-describedby': 'category-help'
        })

    def is_valid(self):
        # force a clean of the form
        self.full_clean()
        return super().is_valid()

    def clean(self):
        # TODO: more validation?
        self._clean_ingredients()
        self._clean_directions()
        return super().clean()

    def _clean_ingredients(self):
        """
        Collect all the ingredient data submitted and verify that it is valid.
        """
        ingredients = {}
        ing_num = 1
        name_field = 'ing_name%d' % ing_num
        # While there is a numbered ingredient name value
        while self.data.get(name_field):
            ing_name = self.data[name_field]
            quantity_field = 'quantity%d' % ing_num

            self.fields[name_field] = forms.CharField()
            self.fields[quantity_field] = forms.IntegerField()

            quantity_val = self.data.get(quantity_field)
            if not quantity_val:
                raise forms.ValidationError(
                    'Missing quantity for ingredient: %(name)',
                    params={'name': ing_name},
                    code='missing_quantity'
                )
            elif int(quantity_val) < 1:
                raise forms.ValidationError(
                    'Invalid value for quantity.',
                    code='invalid_quantity'
                )
            else:
                ingredients[ing_num] = IngredientData(name=ing_name, quantity=self.data[quantity_field])

            # create the ingredient if it doesn't exist in the db
            if IngredientName.objects.filter(name=ing_name).count() == 0:
                IngredientName.objects.create(
                    created_at=timezone.now(),
                    name=ing_name
                )

            ing_num += 1
            name_field = 'ing_name%d' % ing_num

        self.cleaned_data['ingredients'] = ingredients

    def _clean_directions(self):
        """
        Collect all the direction data submitted and verify that it is valid.
        """
        directions = {}
        dir_num = 1
        text_field = 'dir_text%d' % dir_num
        while self.data.get(text_field):
            dir_text = self.data[text_field]
            self.fields[text_field] = forms.CharField()

            if len(dir_text) > 1000:
                raise forms.ValidationError(
                    'Directions cannot be larger than 1000 characters.',
                    code='invalid_direction'
                )

            directions[dir_num] = dir_text
            dir_num += 1
            text_field = 'dir_text%d' % dir_num

        self.cleaned_data['directions'] = directions

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.created_at = timezone.now()
        recipe.prep_time = '%s %s' % (self.cleaned_data['prep_time_num'], self.cleaned_data['prep_time_unit'])
        recipe.cook_time = '%s %s' % (self.cleaned_data['cook_time_num'], self.cleaned_data['cook_time_unit'])
        if commit:
            recipe.save()
        return recipe

    def save_ingredients(self, recipe):
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
                index=ingNum
            )

    def save_directions(self, recipe):
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
                recipe=recipe
            )

    class Meta:
        model = Recipe
        fields = ('name', 'summary', 'servings', 'calories', 'categories', 'image')


class ReviewRecipeForm(forms.ModelForm):

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and rating < settings.REVIEWS['rating_min'] or rating > settings.REVIEWS['rating_max']:
            raise forms.ValidationError('The rating is out of bounds.', code='invalid_rating')
        return rating

    class Meta:
        model = Review
        fields = ('rating', 'text')


class SearchForm(forms.Form):
    q = forms.CharField(required=True)
