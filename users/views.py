#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 18:47.
from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from recipes.models import RecipeModel
from recipes.serializers import RecipeSerializer
from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ReadOnlyUserView(generics.RetrieveAPIView):
    """Retrieves the user profile"""

    lookup_field = 'username'
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserRecipesView(generics.ListAPIView):
    """Lists all recipes a user has"""

    serializer_class = RecipeSerializer

    def get_queryset(self):
        return RecipeModel.objects.filter(user__username=self.kwargs['username'])


class UserFavouritesView(generics.ListAPIView):
    """Lists all favourited recipes a user has"""

    serializer_class = RecipeSerializer

    def get_queryset(self):
        return get_user_model().objects.get(username=self.kwargs['username']).favorites


class UserFollowersView(generics.ListAPIView):
    """Lists all followers a user has"""

    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return get_user_model().objects.get(username=self.kwargs['username']).followed_by


class UserFollowingsView(generics.ListAPIView):
    """Lists all followings a user has"""

    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return get_user_model().objects.get(username=self.kwargs['username']).follows


class FollowView(APIView):
    """View for adding or deleting a user from your followings list"""

    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, username):
        return get_object_or_404(self.queryset, username=username)

    def post(self, request, username):
        user_follwed = self.get_object(username)
        user_follower = request.user
        user_follower.follow(user_follwed)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        user_follwed = self.get_object(username)
        user_follower = request.user
        if user_follower.is_following(user_follwed):
            user_follower.unfollow(user_follwed)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(_("The selected user is not in your followings list."),
                        status=status.HTTP_400_BAD_REQUEST)
