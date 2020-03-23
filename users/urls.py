#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 13:54.

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    # path('<username>/'),
    # path('<username>/recipes/'),
    # path('<username>/favourites/'),
    # path('<username>/follow/'),
    # path('<username>/followers/'),
    # path('<username>/following/'),
]
