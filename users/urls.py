#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 17:22.

from django.urls import path

from users.views import ReadOnlyUserView, UserRecipesView, UserFavouritesView, UserFollowersView, UserFollowingsView, \
    FollowView
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('<username>/', ReadOnlyUserView.as_view(), name='user-profile'),
    path('<username>/recipes/', UserRecipesView.as_view(), name='user-recipes'),
    path('<username>/favourites/', UserFavouritesView.as_view(), name='user-favourites'),
    path('<username>/follow/', FollowView.as_view(), name='user-follow'),
    path('<username>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('<username>/followings/', UserFollowingsView.as_view(), name='user-followings'),
]
