#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 13:54.
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import RecipesFeedView, RecipesView, FavouriteView

app_name = 'recipes'

recipes_router = DefaultRouter()
recipes_router.register('', RecipesView, basename='recipes')

urlpatterns = [
    path('feed/', RecipesFeedView.as_view(), name='feed'),
    path('', include(recipes_router.urls)),
    # path('<slug:slug>/images/'),
    path('<slug:slug>/favourite/', FavouriteView.as_view(), name='favourite'),
    # path('tags/<name>/')
]
