from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('recipes', views.RecipeViewSet)
router.register('categories', views.CategoryViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls))
]
