from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from core.forms.users import SearchForm, IngredientSearchForm
from core.models import Recipe
from core.utils import RawQueries


def index(request):
    """
    Displays the main content view with recipes with the __featured__ flag set to True.
    """
    recipe_list = Recipe.objects.filter(is_featured=True).order_by('-created_at')
    return render(request, 'core/main/featured.html', {'recipe_list': recipe_list, 'explore': 'featured'})


def popular(request):
    """
    Displays the main content view with "popular" recipes. A recipes is considered "popular" if it has at least the
    amount of reviews as configured and has a average rating of at least the configured value.
    """
    recipe_list = Recipe.objects.raw(
        RawQueries.popular_select,
        [settings.POPULAR['rating_threshold'], settings.POPULAR['review_count_threshold']]
    )
    return render(request, 'core/main/popular.html', {'recipe_list': recipe_list, 'explore': 'popular'})


def trending(request):
    """
    Displays the main content view with "trending" recipes. A recipes is considered "trending" when it has received the
    configured amount of review within the configured time window.
    """
    recipe_list = Recipe.objects.raw(
        RawQueries.trending_select,
        [settings.TRENDING['time_window'], settings.TRENDING['review_count']]
    )
    return render(request, 'core/main/trending.html', {'recipe_list': recipe_list, 'explore': 'trending'})


def new(request):
    """
    Displays the main content view with new recipes. A recipes is considered new when it's age is younger than the
    configured value.
    """
    time_cutoff = timezone.now() - timezone.timedelta(seconds=settings.NEW['time_window'])
    recipe_list = Recipe.objects.filter(created_at__gt=time_cutoff).order_by('-created_at')
    return render(request, 'core/main/new.html', {'recipe_list': recipe_list, 'explore': 'new'})


def search(request):
    """
    Submits a search query and returns a list of the resulting recipes.
    """
    form = SearchForm(request.GET)
    if form.is_valid():
        recipe_list = form.result_set()
    else:
        recipe_list = []
    return render(request, 'core/main/search_results.html', {'recipe_list': recipe_list, 'form': form})


def ingredient_search(request):
    """
    Displays the "ingredient search" view.
    """
    return render(request, 'core/main/ingredient_search.html')


def ingredient_search_results(request):
    """
    Submits and displays the results of an "ingredient search".
    """
    form = IngredientSearchForm(request.GET)
    if form.is_valid():
        recipes = form.match_recipes()
    else:
        recipes = []
    return render(request, 'core/main/ingredient_search_results.html', {'recipe_list': recipes})
