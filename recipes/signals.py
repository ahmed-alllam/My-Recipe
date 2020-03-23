#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 18:47.
import re

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from recipes.models import RecipeModel


def _slug_strip(value):
    """removes the '-' separator from the end or start of the string"""
    return re.sub(r'^%s+|%s+$' % ('-', '-'), '', value)


def unique_slugify(instance, value):
    """function used to give a unique slug to an instance"""

    slug = slugify(value)
    slug = slug[:255]  # limit its len to max_length of slug field

    slug = _slug_strip(slug)
    original_slug = slug

    queryset = instance.__class__.objects.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    _next = 2
    while not slug or queryset.filter(slug=slug):
        slug = original_slug
        end = '-%s' % _next
        if len(slug) + len(end) > 255:
            slug = slug[:255 - len(end)]
            slug = _slug_strip(slug)
        slug = '%s%s' % (slug, end)
        _next += 1

    return slug


@receiver(pre_save, sender=RecipeModel)
def add_slug_to_recipe(instance, **kwargs):
    """The receiver called before a recipe is saved
    to give it a unique slug"""

    instance.slug = unique_slugify(instance, instance.name)
