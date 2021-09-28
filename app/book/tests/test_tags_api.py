from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Book

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

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        # Make HTTP request to create Tag
        self.client.post(TAGS_URL, payload)

        # Verify if the tag exists
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        # Make HTTP request to create Tag
        res = self.client.post(TAGS_URL, payload)

        # Chech that the request failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_books(self):
        """Test filtering tags by those assigned to books"""
        # Create tags
        tag1 = Tag.objects.create(user=self.user, name='Historical')
        tag2 = Tag.objects.create(user=self.user, name='Biography')
        # Create book with tags
        book = Book.objects.create(
            title='Tom Clancy',
            pages=100,
            year=1995,
            price=5.00,
            user=self.user
        )
        book.tags.add(tag1)

        # Make HTTP request to get tags that are linked to
        # at least one book
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        # Get JSON for the tag objects
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        # Check that only the tag1 is returned
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tags by assigned returns unique items"""
        # Create tag
        tag = Tag.objects.create(user=self.user, name='Mistery')
        Tag.objects.create(user=self.user, name='Crime')
        # Create book and add tag
        book1 = Book.objects.create(
            title='The Handmaid\'s tale',
            pages=300,
            year=1992,
            price=3.00,
            user=self.user
        )
        book1.tags.add(tag)
        # Create book and add tag
        book2 = Book.objects.create(
            title='Why Karl Marx Was Right',
            pages=500,
            year=1900,
            price=2.00,
            user=self.user
        )
        book2.tags.add(tag)

        # Make HTTP request to get tags that are linked to
        # at least one book
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        # Check that only one tag is received
        self.assertEqual(len(res.data), 1)
