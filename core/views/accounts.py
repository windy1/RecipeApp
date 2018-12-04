from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from core.forms.users import SignUpForm, SaveUserProfileForm
from core.models import UserProfile


def signup(request):
    """
    Submits the form to register for the site.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            UserProfile.objects.create(created_at=timezone.now(), user=user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def preferences(request):
    """
    Either displays the preferences page or saves the user's preferences if GET or POST request respectively.
    """
    profile, created = UserProfile.get_or_create(request.user)
    saved = False
    if request.method == 'POST':
        # users is saving their preferences
        form = SaveUserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            saved = True
    else:
        form = SaveUserProfileForm(instance=profile)
    context = {'profile': profile, 'form': form, 'saved': saved, 'explore': 'preferences'}
    return render(request, 'core/accounts/preferences.html', context)
