#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 13:54.

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    name = 'recipes'

    def ready(self):
        import recipes.signals
