#  Copyright (c) Code Written and Tested by Ahmed Emad in 16/03/2020, 21:38.

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """UnitTest for models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='test123')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="test123")

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'normal@user.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_create_superuser(self):
        """test for creating a super user"""

        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'test123')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
