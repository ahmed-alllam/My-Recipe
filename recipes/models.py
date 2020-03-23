#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 13:54.

import uuid

from django.contrib.auth import get_user_model
from django.db import models


def image_upload(instance, filename):
    """Gives a unique path to the saved user photo in models.
    Arguments:
        instance: the model instance itself, it is not
                  used in thisfunction but it's required by django.
        filename: the name of the photo sent by user, it's
                  used here to get the format of the photo.
    Returns:
        The unique path that the photo will be stored in the DB.
    """
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
    timestamp = models.DateTimeField()  # time of publishing

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.name

    @property
    def favourites_count(self):
        """gets the favourites count for that recipes"""
        return self.favorited_by.count()


class TagModel(models.Model):
    """Model for Recipe tags"""
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag


class IngredientModel(models.Model):
    """Model for Recipe Ingredients"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    recipe = models.ForeignKey(to=RecipeModel, on_delete=models.CASCADE, related_name='ingredients')

    # todo : add unique together

    def __str__(self):
        return self.name


class ImageModel(models.Model):
    """An alias to imagefield to enable a recipe to have many images"""
    image = models.ImageField(upload_to=image_upload)
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    recipe = models.ForeignKey(to=RecipeModel, on_delete=models.CASCADE, related_name='images')
