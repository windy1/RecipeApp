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
    path('ingredient-search', main.ingredient_search, name='ingredient_search'),
    path('ingredient-search/results', main.ingredient_search_results, name='ingredient_search_results'),

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
    path('recipes/<int:recipe_id>/edit', recipes.edit_recipe, name='edit_recipe'),

    path('api/', include('api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
