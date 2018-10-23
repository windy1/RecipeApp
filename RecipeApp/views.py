from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import Recipe


def index(request):
    recipeList = Recipe.objects.filter(is_featured=True).order_by('-created_at')
    return render(request, 'RecipeApp/featured.html', {'recipeList': recipeList, 'explore': 'featured'})


def popular(request):
    return render(request, 'RecipeApp/popular.html', {'explore': 'popular'})


def categories(request):
    return render(request, 'RecipeApp/categories.html', {'explore': 'categories'})


def new(request):
    return render(request, 'RecipeApp/new.html', {'explore': 'new'})


def trending(request):
    return render(request, 'RecipeApp/trending.html', {'explore': 'trending'})


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
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipeId)
    ingredients = recipe.ingredient_set.order_by('-index')
    directions = recipe.direction_set.order_by('-index')
    canReview = user.is_authenticated and Review.objects.filter(user=user, recipe=recipe).count() == 0
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'directions': directions,
        'canReview': canReview
    }
    return render(request, 'RecipeApp/recipeDetail.html', context)


@login_required
def review(request, recipeId):
    recipe = get_object_or_404(Recipe, pk=recipeId)
    if request.method == 'POST':
        form = ReviewRecipeForm(request.POST)
        if form.is_valid():
            rvw = form.save(commit=False)
            rvw.created_at = timezone.now()
            rvw.user = request.user
            rvw.recipe = recipe
            rvw.save()
    return redirect('recipeDetail', recipe.id)


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
            recipe.save()
            form.createIngredients(recipe)
            form.createDirections(recipe)
            return redirect('myRecipes', request.user.username)
    else:
        form = SubmitRecipeForm()
    return render(request, 'RecipeApp/submitRecipe.html', {'form': form})
