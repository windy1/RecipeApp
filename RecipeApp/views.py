from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import Recipe


def index(request):
    recipe_list = Recipe.objects.filter(is_featured=True).order_by('-created_at')
    return render(request, 'RecipeApp/featured.html', {'recipe_list': recipe_list, 'explore': 'featured'})


def popular(request):
    recipe_list = Recipe.objects.filter(
        review_count__gte=settings.POPULAR['review_count_threshold'],
        avg_rating__gte=settings.POPULAR['rating_threshold']
    )
    return render(request, 'RecipeApp/popular.html', {'recipe_list': recipe_list, 'explore': 'popular'})


def categories(request):
    category_list = Category.objects.filter(parent=None)
    return render(request, 'RecipeApp/category/category_list.html', {'category_list': category_list, 'explore': 'category'})


def category_detail(request, name):
    category = get_object_or_404(Category, name=name)
    sub_categories = Category.objects.filter(parent=category).order_by('-name')
    context = {'category': category, 'explore': 'category'}

    if sub_categories.count() > 0:
        context['category_list'] = sub_categories
        return render(request, 'RecipeApp/category/category_list.html', context)

    context['recipe_list'] = category.recipe_set.order_by('-avg_rating')
    return render(request, 'RecipeApp/category/category_detail.html', context)


def new(request):
    time_cutoff = timezone.now() - timezone.timedelta(seconds=settings.NEW['time_window'])
    recipe_list = Recipe.objects.filter(created_at__gt=time_cutoff).order_by('-created_at')
    return render(request, 'RecipeApp/new.html', {'recipe_list': recipe_list, 'explore': 'new'})


def trending(request):
    recipe_list = Recipe.objects.filter(trending_count__gte=settings.TRENDING['review_count'])
    return render(request, 'RecipeApp/trending.html', {'recipe_list': recipe_list, 'explore': 'trending'})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def recipe_detail(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredient_set.order_by('-index')
    directions = recipe.direction_set.order_by('-index')
    can_review = (user.is_authenticated and Review.objects.filter(user=user, recipe=recipe).count() == 0) or True
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'directions': directions,
        'can_review': can_review
    }
    return render(request, 'RecipeApp/recipe/recipe_detail.html', context)


@login_required
def review(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
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

            trending_cutoff = timezone.now() - timezone.timedelta(seconds=settings.TRENDING['time_window'])
            recipe.trending_count = recipe.review_set.filter(created_at__gt=trending_cutoff).count()

            recipe.save()

            # TODO: Update trending_count periodically in the background as it will need to change as time passes

    return redirect('recipeDetail', recipe.id)


def my_recipes(request, username):
    user = get_object_or_404(User, username=username)
    recipes = user.recipe_set.all()
    return render(request, 'RecipeApp/user/my_recipes.html', {'recipe_list': recipes, 'explore': 'myRecipes'})


@login_required
def submit(request):
    if request.method == 'POST':
        form = SubmitRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            recipe.categories.set(form.cleaned_data['categories'])
            form.create_ingredients(recipe)
            form.create_directions(recipe)
            return redirect('my_recipes', request.user.username)
    else:
        form = SubmitRecipeForm()
    return render(request, 'RecipeApp/recipe/submit_recipe.html', {'form': form})
