from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        """Info about how to serialize the user model"""
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Extra requirements for the user model
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # validation_data: JSON data passed in the HTTP POST
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it
            - instance: the user object
            - validated_data: JSON object from the HTTP request
        """
        # Get password, remove from the original dictionary
        password = validated_data.pop('password', None)
        # Update user, and get user
        user = super().update(instance, validated_data)

        # Update user's password
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""

        # attrs: dictionary for the fields that make up the serializer
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # The user was not authenticated (the authentication fails)
        if not user:
            # underscore for translation
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
