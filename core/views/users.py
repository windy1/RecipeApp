from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from core.models import UserProfile


def user_profile(request, username):
    """
    Displays the user profile of the user with the specified username.
    """
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.get_or_create(user)
    errors = request.session.pop('form_errors', None)
    context = {'profile': profile, 'form_errors': errors, 'explore': 'user_profile'}
    return render(request, 'core/users/user_profile.html', context)


def user_recipes(request, username):
    """
    Displays a list of all recipes created by the users as specified in the URL.
    """
    user = get_object_or_404(User, username=username)
    recipes = user.recipe_set.all()
    context = {'recipe_list': recipes, 'user': user, 'explore': 'user_recipes'}
    return render(request, 'core/users/user_recipes.html', context)
