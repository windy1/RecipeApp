from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden

from core.forms.recipes import ReviewRecipeForm, SubmitRecipeForm
from core.models import Recipe


def recipe_detail(request, recipe_id):
    """
    Displays a detailed view of the recipes as specified in the URL.
    """
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredient_set.order_by('-index')
    directions = recipe.direction_set.order_by('-index')
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'directions': directions,
        'can_review': recipe.user_can_review(user)
    }
    return render(request, 'core/recipes/recipe_detail.html', context)


@login_required
def submit_review(request, recipe_id):
    """
    Submits a review for the recipes as specified in the URL.
    """
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


@login_required
def submit_recipe(request):
    """
    Submits a new recipes for creation.
    """
    if request.method == 'POST':
        form = SubmitRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            recipe.categories.set(form.cleaned_data['categories'])
            form.save_ingredients(recipe)
            form.save_directions(recipe)
            return redirect('recipe_detail', recipe.id)
    else:
        form = SubmitRecipeForm()
    return render(request, 'core/recipes/recipe_submit.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    """
    Submits changes to an already created recipe.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.user:
        return HttpResponseForbidden()
    return render(request, 'core/recipes/recipe_edit.html', {'recipe': recipe})
