from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import Recipe


def index(request):
    recipe_list = Recipe.objects.filter(is_featured=True).order_by('-created_at')
    return render(request, 'core/featured.html', {'recipe_list': recipe_list, 'explore': 'featured'})


def popular(request):
    recipe_list = Recipe.objects.raw(
        """
        SELECT   rec.*, AVG(rev.rating) AS avg_rating, COUNT(rev.id) AS review_count 
        FROM     core_recipe AS rec
        JOIN     core_review AS rev ON rev.recipe_id = rec.id
        GROUP BY rec.id
        HAVING   avg_rating >= %s
        AND      review_count >= %s
        ORDER BY review_count DESC, avg_rating DESC
        """,
        [settings.POPULAR['rating_threshold'], settings.POPULAR['review_count_threshold']]
    )
    return render(request, 'core/popular.html', {'recipe_list': recipe_list, 'explore': 'popular'})


def trending(request):
    # FIXME
    recipe_list = []
    return render(request, 'core/trending.html', {'recipe_list': recipe_list, 'explore': 'trending'})


def new(request):
    time_cutoff = timezone.now() - timezone.timedelta(seconds=settings.NEW['time_window'])
    recipe_list = Recipe.objects.filter(created_at__gt=time_cutoff).order_by('-created_at')
    return render(request, 'core/new.html', {'recipe_list': recipe_list, 'explore': 'new'})


def categories(request):
    category_list = Category.objects.filter(parent=None)
    context = {'category_list': category_list, 'explore': 'category'}
    return render(request, 'core/category/category_list.html', context)


def category_detail(request, name):
    category = get_object_or_404(Category, name=name)
    sub_categories = Category.objects.filter(parent=category).order_by('-name')
    context = {'category': category, 'explore': 'category'}

    if sub_categories.count() > 0:
        # if the category has no sub-categories, list out the recipes in that category
        context['category_list'] = sub_categories
        return render(request, 'core/category/category_list.html', context)

    # list the category's sub-categories
    context['recipe_list'] = category.recipe_set.order_by('-avg_rating')
    return render(request, 'core/category/category_detail.html', context)


def recipe_detail(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredient_set.order_by('-index')
    directions = recipe.direction_set.order_by('-index')
    can_review = (user.is_authenticated and Review.objects.filter(user=user, recipe=recipe).count() == 0)  or True
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'directions': directions,
        'can_review': can_review
    }
    return render(request, 'core/recipe/recipe_detail.html', context)


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
            recipe.save()
    return redirect('recipe_detail', recipe.id)


def user_recipes(request, username):
    user = get_object_or_404(User, username=username)
    recipes = user.recipe_set.all()
    return render(request, 'core/user/user_recipes.html', {'recipe_list': recipes, 'explore': 'user_recipes'})


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['q']
        recipe_list = Recipe.objects.filter(
            Q(name__icontains=query) | Q(user__username__icontains=query) | Q(summary__icontains=query)
        )
    else:
        recipe_list = []
    return render(request, 'core/search_results.html', {'recipe_list': recipe_list})


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
            return redirect('user_recipes', request.user.username)
    else:
        form = SubmitRecipeForm()
    return render(request, 'core/recipe/submit_recipe.html', {'form': form})


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
