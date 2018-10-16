from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate

from .models import Recipe
from .forms import SignUpForm


def index(request):
    recipeList = Recipe.objects.order_by('-created_at')
    return render(request, 'RecipeApp/index.html', {'recipeList': recipeList})


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
