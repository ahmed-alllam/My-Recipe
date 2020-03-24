#  Copyright (c) Code Written and Tested by Ahmed Emad in 24/03/2020, 14:36.
from rest_framework import permissions

from recipes.models import RecipeModel, RecipeImageModel, RecipeReviewModel


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if type(obj) == RecipeModel or type(obj) == RecipeReviewModel:
            return obj.user == request.user
        elif type(obj) == RecipeImageModel:
            return obj.recipe.user == request.user
        return False
