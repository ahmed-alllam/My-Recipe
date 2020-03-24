#  Copyright (c) Code Written and Tested by Ahmed Emad in 24/03/2020, 14:36.

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'name', 'bio', 'image')
        extra_kwargs = {
            'password': {
                'write_only': True, 'min_length': 5
            },
            'username': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        email = validated_data.get('email', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)

        if email:
            username = email.split('@')[0] + uuid.uuid4().hex[:10]
            while User.objects.filter(username=username):
                username = email.split('@')[0] + uuid.uuid4().hex[:10]
            user.username = username

        if email or password:
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={
            'input_type': 'password'
        },
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
