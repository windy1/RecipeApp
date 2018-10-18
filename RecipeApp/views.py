from enum import Enum

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Recipe
from .forms import SignUpForm, SubmitRecipeForm


def index(request):
    recipeList = Recipe.objects.order_by('-created_at')
    return render(request, 'RecipeApp/featured.html', {'recipeList': recipeList, 'explore': 'featured'})


def categories(request):
    return render(request, 'RecipeApp/categories.html', {'explore': 'categories'})


def new(request):
    return render(request, 'RecipeApp/new.html', {'explore': 'new'})


def trending(request):
    return render(request, 'RecipeApp/trending.html', {'explore': 'trending'})


def popular(request):
    return render(request, 'RecipeApp/popular.html', {'explore': 'popular'})


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signUp.html', {'form': form})


def recipeDetail(request, recipeId):
    recipe = get_object_or_404(Recipe, pk=recipeId)
    return render(request, 'RecipeApp/recipeDetail.html', {'recipe': recipe})


def myRecipes(request, username):
    user = get_object_or_404(User, username=username)
    recipes = user.recipe_set.all()
    return render(request, 'RecipeApp/myRecipes.html', {'recipeList': recipes, 'explore': 'myRecipes'})


@login_required
def submit(request):
    if request.method == 'POST':
        form = SubmitRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.created_at = timezone.now()
            recipe.save()
            return redirect('myRecipes', request.user.username)
    else:
        form = SubmitRecipeForm()
    return render(request, 'RecipeApp/submitRecipe.html', {'form': form})
