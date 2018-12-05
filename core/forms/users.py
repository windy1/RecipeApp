from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from core.models import UserProfile, IngredientName, Recipe, Ingredient


class SignUpForm(UserCreationForm):
    """
    Form submitted when a users signs up for a new account

    See: templates/registration/signup.html template
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


class SaveUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('image', 'bio')


class SearchForm(forms.Form):
    q = forms.CharField(required=True)

    def result_set(self):
        assert self.is_valid()
        query = self.cleaned_data['q']
        return Recipe.objects.filter(
            Q(name__icontains=query) | Q(user__username__icontains=query) | Q(summary__icontains=query)
        )


class IngredientSearchForm(forms.Form):
    ingredients = forms.CharField(max_length=1024, required=True)

    def match_recipes(self):
        q = Ingredient.objects.filter(ingredient__in=self.ingredient_set()).select_related('recipe')
        return set(_.recipe for _ in q)

    def ingredient_set(self):
        assert self.is_valid()
        val = self.cleaned_data['ingredients']
        ing_list = []
        for ing_name in val.split(','):
            try:
                ing_list.append(IngredientName.objects.get(name=ing_name))
            except ObjectDoesNotExist:
                pass
        return ing_list
