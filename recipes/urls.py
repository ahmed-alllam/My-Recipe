#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 18:47.
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import RecipesFeedView, RecipesView, FavouriteView, TagFeedView, RecipeImageView

app_name = 'recipes'

recipes_router = DefaultRouter()
recipes_router.register('', RecipesView, basename='recipes')

recipe_images_router = DefaultRouter()
recipe_images_router.register('', RecipeImageView, basename='recipe-images')

urlpatterns = [
    path('feed/', RecipesFeedView.as_view(), name='feed'),
    path('', include(recipes_router.urls)),
    path('<slug:slug>/images/', include(recipe_images_router.urls)),
    path('<slug:slug>/favourite/', FavouriteView.as_view(), name='favourite'),
    path('tags/<name>/', TagFeedView.as_view(), name='tag-feed')
]
