"""RecipeApp URL Configuration

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

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    path('featured/', views.index, name='featured'),
    path('popular/', views.popular, name='popular'),
    path('trending/', views.trending, name='trending'),
    path('new/', views.new, name='new'),

    path('categories/', views.categories, name='categories'),
    path('categories/<name>/', views.category_detail, name='category_detail'),

    path('submit/', views.submit, name='submit'),

    path('u/<username>/recipes/', views.my_recipes, name='my_recipes'),

    path('r/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('r/<int:recipe_id>/review', views.review, name='review'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.sign_up, name='signup'),

    path('api/', include('RecipeAPI.urls'))
]
