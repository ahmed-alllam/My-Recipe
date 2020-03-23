#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 17:22.

from itertools import chain

from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import gettext_lazy as _

from recipes.models import RecipeModel
from recipes.permission import IsOwnerOrReadOnly
from recipes.serializers import RecipeSerializer, DetailedRecipeSerializer


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
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

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
