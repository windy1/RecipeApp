from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import Recipe


def index(request):
    recipeList = Recipe.objects.filter(is_featured=True).order_by('-created_at')
    return render(request, 'RecipeApp/featured.html', {'recipeList': recipeList, 'explore': 'featured'})


def popular(request):
    recipeList = Recipe.objects.filter(
        review_count__gte=settings.POPULAR['review_count_threshold'],
        avg_rating__gte=settings.POPULAR['rating_threshold'])
    return render(request, 'RecipeApp/popular.html', {'recipeList': recipeList, 'explore': 'popular'})


def categories(request):
    return render(request, 'RecipeApp/categories.html', {'explore': 'categories'})


def new(request):
    timeCutoff = timezone.now() - timezone.timedelta(seconds=settings.NEW['time_window'])
    recipeList = Recipe.objects.filter(created_at__gt=timeCutoff).order_by('-created_at')
    return render(request, 'RecipeApp/new.html', {'recipeList': recipeList, 'explore': 'new'})


def trending(request):
    recipeList = Recipe.objects.filter(trending_count__gte=settings.TRENDING['review_count'])
    return render(request, 'RecipeApp/trending.html', {'recipeList': recipeList, 'explore': 'trending'})


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
    canReview = (user.is_authenticated and Review.objects.filter(user=user, recipe=recipe).count() == 0) or True
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

            recipe.review_count = recipe.review_set.count()
            recipe.avg_rating = recipe.review_set.aggregate(Avg('rating'))['rating__avg']

            trendingCutoff = timezone.now() - timezone.timedelta(seconds=settings.TRENDING['time_window'])
            recipe.trending_count = recipe.review_set.filter(created_at__gt=trendingCutoff).count()

            recipe.save()

            # TODO: Update trending_count periodically in the background as it will need to change as time passes

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
