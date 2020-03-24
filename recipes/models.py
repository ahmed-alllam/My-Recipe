#  Copyright (c) Code Written and Tested by Ahmed Emad in 24/03/2020, 14:43.

import uuid

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models import Avg


def image_upload(instance, filename):
    """Gives a unique path to the saved user photo in models"""
    return 'images/{0}{1}'.format(uuid.uuid4().hex, filename)


class RecipeModel(models.Model):
    """Model for the User Recipe"""
    user = models.ForeignKey(to=get_user_model(), related_name='recipes', on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='recipes.TagModel', related_name='recipes')
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    body = models.TextField()
    main_image = models.ImageField(upload_to=image_upload, null=True)
    time_to_finish = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # time of publishing

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.name

    @property
    def favourites_count(self):
        """gets the favourites count for that recipes"""
        return self.favorited_by.count()

    @property
    def reviews_count(self):
        """gets the reviews count for that recipes"""
        return self.reviews.count()

    @property
    def rating(self):
        """gets the rating of that recipe from its reviews"""
        return self.reviews.all().aggregate(Avg('rating')).get('rating__avg', '')


class TagModel(models.Model):
    """Model for Recipe tags"""
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag


class IngredientModel(models.Model):
    """Model for Recipe Ingredients"""
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(to=RecipeModel, on_delete=models.CASCADE, related_name='ingredients')

    class Meta:
        unique_together = ('recipe', 'name')  # to prevent having duplicate ingredients in one recipe

    def __str__(self):
        return self.name


class RecipeImageModel(models.Model):
    """An alias to image field to enable a recipe to have many images"""
    image = models.ImageField(upload_to=image_upload)
    recipe = models.ForeignKey(to=RecipeModel, on_delete=models.CASCADE, related_name='images')


class RecipeReviewModel(models.Model):
    """Model for Recipe Reviews"""
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(to=RecipeModel, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, max_length=255)
    rating = models.PositiveIntegerField(validators=[
        validators.MaxValueValidator(5),
        validators.MinValueValidator(1),
    ])
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # time of commenting

    class Meta:
        unique_together = ('recipe', 'slug')
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title
