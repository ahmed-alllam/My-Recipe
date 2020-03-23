#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 21:18.
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj.recipe.user == request.user
