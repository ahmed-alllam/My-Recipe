#  Copyright (c) Code Written and Tested by Ahmed Emad in 23/03/2020, 13:54.
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.utils.translation import gettext_lazy as _


def user_upload(instance, filename):
    """Gives a unique path to the saved user photo in models.
    Arguments:
        instance: the model instance itself, it is not
                  used in thisfunction but it's required by django.
        filename: the name of the photo sent by user, it's
                  used here to get the format of the photo.
    Returns:
        The unique path that the photo will be stored in the DB.
    """
    return 'users/{0}{1}'.format(uuid.uuid4().hex, filename)


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(email=self.normalize_email(email), **extra_fields)

        username = email.split('@')[0] + uuid.uuid4().hex[:10]
        while User.objects.filter(username=username):
            username = email.split('@')[0] + uuid.uuid4().hex[:10]

        user.username = username
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    username = models.CharField(max_length=300, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=user_upload)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )
    favorites = models.ManyToManyField(
        'recipes.RecipeModel',
        related_name='favorited_by'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def follow(self, user):
        """Follow `user` if we're not already following `user`."""
        self.follows.add(user)

    def unfollow(self, user):
        """Unfollow `user` if we're already following `user`."""
        self.follows.remove(user)

    def is_following(self, user):
        """Returns True if we're following `user`; False otherwise."""
        return self.follows.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        """Returns True if `user` is following us; False otherwise."""
        return self.followed_by.filter(pk=user.pk).exists()

    def favorite(self, recipe):
        """Favorite `recipe` if we haven't already favorited it."""
        self.favorites.add(recipe)

    def unfavorite(self, recipe):
        """Unfavorite `recipe` if we've already favorited it."""
        self.favorites.remove(recipe)

    def has_favorited(self, recipe):
        """Returns True if we have favorited `recipe`; else False."""
        return self.favorites.filter(pk=recipe.pk).exists()
