#  Copyright (c) Code Written and Tested by Ahmed Emad in 24/03/2020, 14:36.

from django.contrib import admin

from recipes.models import RecipeImageModel, IngredientModel, TagModel, RecipeModel, RecipeReviewModel


class RecipeModelAdmin(admin.ModelAdmin):
    """Admin For Recipe model"""
    list_display = ('user', 'name', 'time_to_finish', 'timestamp')


class TagModelAdmin(admin.ModelAdmin):
    """Admin For Tag model"""
    list_display = ('tag',)


class IngredientModelAdmin(admin.ModelAdmin):
    """Admin For Ingredient model"""
    list_display = ('name',)


class ImageModelAdmin(admin.ModelAdmin):
    """Admin For Recipe Image model"""
    list_display = ('image', 'recipe')


class RecipeReviewModelAdmin(admin.ModelAdmin):
    """Admin For Recipe Review model"""
    list_display = ('user', 'recipe', 'title', 'rating', 'timestamp')


admin.site.register(RecipeModel, RecipeModelAdmin)
admin.site.register(TagModel, TagModelAdmin)
admin.site.register(IngredientModel, IngredientModelAdmin)
admin.site.register(RecipeImageModel, ImageModelAdmin)
admin.site.register(RecipeReviewModel, RecipeReviewModelAdmin)
