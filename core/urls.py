"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import categories, main, recipes, accounts, users


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', main.index, name='index'),
    path('featured/', main.index, name='featured'),
    path('popular/', main.popular, name='popular'),
    path('trending/', main.trending, name='trending'),
    path('new/', main.new, name='new'),
    path('search/', main.search, name='search'),

    path('accounts/signup/', accounts.signup, name='signup'),
    path('accounts/preferences/', accounts.preferences, name='preferences'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('users/<username>/', users.user_profile, name='user_profile'),
    path('users/<username>/recipes/', users.user_recipes, name='user_recipes'),

    path('categories/', categories.categories, name='categories'),
    path('categories/<name>/', categories.category_detail, name='category_detail'),

    path('submit/', recipes.submit_recipe, name='submit_recipe'),
    path('recipes/<int:recipe_id>/', recipes.recipe_detail, name='recipe_detail'),
    path('recipes/<int:recipe_id>/review', recipes.submit_review, name='submit_review'),

    path('api/', include('api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
