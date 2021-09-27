from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from book.serializers import TagSerializer


TAGS_URL = reverse('book:tag-list')


class PublicTagsApiTests(TestCase):
    """Test thje publicly available tags API"""

    def setUp(self):
        # Create API Client
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        # Make HTTP request to get tags
        res = self.client.get(TAGS_URL)

        # Check that the request failed with unauthorized status
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        # Create and authenticate user
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        # Create tags on the db
        Tag.objects.create(user=self.user, name='Horror')
        Tag.objects.create(user=self.user, name='Comedy')

        # Make HTTPs request to get the tags
        res = self.client.get(TAGS_URL)

        # Obtains tags created earlier ordered by name
        tags = Tag.objects.all().order_by('-name')
        # Obtain the tags as JSON
        # many=True, to indicate that there is more than one object
        serializer = TagSerializer(tags, many=True)
        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that the response data coincedes with the JSON object
        # from the db
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        # Create a new user
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        # Add a tag to the db, created by user2
        Tag.objects.create(user=user2, name='History')
        # Add tag to the db, created by user
        tag = Tag.objects.create(user=self.user, name='Science')

        # Make HTTP request to get tags
        res = self.client.get(TAGS_URL)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that there is only one tag
        self.assertEqual(len(res.data), 1)
        # Check that the tag is the one created by user
        self.assertEqual(res.data[0]['name'], tag.name)
