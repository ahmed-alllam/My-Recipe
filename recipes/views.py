#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 21:18.

from itertools import chain

from django.http import Http404
from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import gettext_lazy as _

from recipes.models import RecipeModel, TagModel, RecipeImageModel
from recipes.permission import IsOwner
from recipes.serializers import RecipeSerializer, DetailedRecipeSerializer, RecipeImageSerializer


class RecipesFeedView(ListAPIView):
    """View for the Recipes Feed"""
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            followings_qs = RecipeModel.objects.filter(user__in=self.request.user.follows.all())
            queryset = list(chain(followings_qs, RecipeModel.objects.all()))
        else:
            queryset = RecipeModel.objects.all()

        return queryset


class RecipesView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """View for creating, updating, retrieving and deleting a Recipe"""

    lookup_field = 'slug'
    serializer_class = DetailedRecipeSerializer
    queryset = RecipeModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner)

    def get_serializer_context(self):
        return {'user': self.request.user}


class FavouriteView(APIView):
    """View for adding or deleting a recipe from your favourites list"""

    queryset = RecipeModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, slug):
        return self.queryset.get(slug=slug)

    def post(self, request, slug):
        recipe = self.get_object(slug)
        user = request.user
        user.favorite(recipe)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        recipe = self.get_object(slug)
        user = request.user
        if user.has_favorited(recipe):
            user.unfavorite(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(_("The selected recipe is not in your favourites list."),
                        status=status.HTTP_400_BAD_REQUEST)


class TagFeedView(ListAPIView):
    """Lists all recipes with a certain tag"""

    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        tag = get_object_or_404(TagModel, tag=self.kwargs['name'])
        return tag.recipes.all()


class RecipeImageView(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """Add or deletes an image from a recipe"""

    lookup_field = 'number'
    serializer_class = RecipeImageSerializer
    queryset = RecipeImageModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        recipe = get_object_or_404(RecipeModel, slug=self.kwargs['slug'])
        if self.action == 'create':
            return recipe
        if self.action == 'destroy':
            number = int(self.kwargs['number']) - 1
            print(recipe.images.count())
            print(number)
            if number >= recipe.images.count() or number < 0:  # bugs
                raise Http404
            return recipe.images.all()[number]

    def perform_create(self, serializer):
        serializer.save(recipe=self.get_object())
