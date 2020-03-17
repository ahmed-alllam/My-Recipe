#  Copyright (c) Code Written and Tested by Ahmed Emad in 17/03/2020, 16:24.

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
