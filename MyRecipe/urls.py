#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 13:54.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
]
