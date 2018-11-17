from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login

from core.models import Recipe
from core.raw_queries import RawQueries
from core.forms import SearchForm, SignUpForm


#Converts any array into a 2D list with n number of elements in each column
def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def index(request):
    recipe_list = Recipe.objects.filter(is_featured=True).order_by('-created_at')
   # recipe_grid = to_matrix(recipe_list, 4)
    return render(request, 'core/featured.html', {'recipe_list': recipe_list, 'explore': 'featured'})


def popular(request):
    recipe_list = Recipe.objects.raw(
        RawQueries.popular_select,
        [settings.POPULAR['rating_threshold'], settings.POPULAR['review_count_threshold']]
    )
    return render(request, 'core/popular.html', {'recipe_list': recipe_list, 'explore': 'popular'})


def trending(request):
    recipe_list = Recipe.objects.raw(
        RawQueries.trending_select,
        [settings.TRENDING['time_window'], settings.TRENDING['review_count']]
    )
    return render(request, 'core/trending.html', {'recipe_list': recipe_list, 'explore': 'trending'})


def new(request):
    time_cutoff = timezone.now() - timezone.timedelta(seconds=settings.NEW['time_window'])
    recipe_list = Recipe.objects.filter(created_at__gt=time_cutoff).order_by('-created_at')
    return render(request, 'core/new.html', {'recipe_list': recipe_list, 'explore': 'new'})


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

