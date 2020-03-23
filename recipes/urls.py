#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 21:18.
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import RecipesFeedView, RecipesView, FavouriteView, TagFeedView, RecipeImageView

app_name = 'recipes'

recipes_router = DefaultRouter()
recipes_router.register('', RecipesView, basename='recipes')

urlpatterns = [
    path('feed/', RecipesFeedView.as_view(), name='feed'),
    path('tags/<name>/', TagFeedView.as_view(), name='tag-feed'),
    path('', include(recipes_router.urls)),
    path('<slug:slug>/images/', RecipeImageView.as_view({'post': 'create'}), name='recipe-images-list'),
    path('<slug:slug>/images/<int:number>/', RecipeImageView.as_view({'delete': 'destroy'}),
         name='recipe-images-detail'),
    path('<slug:slug>/favourite/', FavouriteView.as_view(), name='favourite'),
]
