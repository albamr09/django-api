from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Author, Book

from book.serializers import AuthorSerializer


AUTHOR_URL = reverse('book:author-list')


class PublicAuthorsApiTests(TestCase):
    """Test the publicly available authors API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        # Make HTTPS get request to the authors endpoint
        res = self.client.get(AUTHOR_URL)

        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorsApiTests(TestCase):
    """Test the private authors API"""

    def setUp(self):
        """Create and authenticate user"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_author_list(self):
        """Test retrieving a list of authors"""
        # Create the authors
        Author.objects.create(user=self.user, name='Dostoevsky')
        Author.objects.create(user=self.user, name='Tolstoy')

        res = self.client.get(AUTHOR_URL)

        # Get the authors we just created
        authors = Author.objects.all().order_by('-name')
        # Get JSON
        serializer = AuthorSerializer(authors, many=True)
        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that the data match
        self.assertEqual(res.data, serializer.data)

    def test_authors_limited_to_user(self):
        """Test that authors for the authenticated user are returend"""
        # Create aux user
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        # Create one author per user
        Author.objects.create(user=user2, name='Quijote')
        author = Author.objects.create(user=self.user, name='Unamuno')

        # Make the HTTP get request
        res = self.client.get(AUTHOR_URL)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that the list contains only one author
        self.assertEqual(len(res.data), 1)
        # Check that the author is the one created by user
        self.assertEqual(res.data[0]['name'], author.name)

    def test_create_author_successful(self):
        """Test create a new author"""
        # Define authors attributes
        payload = {'name': 'Margit'}
        # Make HTTP request to create author
        self.client.post(AUTHOR_URL, payload)

        # Check if author was stored on db
        exists = Author.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_author_invalid(self):
        """Test creating invalid author fails"""
        payload = {'name': ''}
        res = self.client.post(AUTHOR_URL, payload)

        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_authors_assigned_to_books(self):
        """Test filtering authors by those assigned to books"""
        # Create authors
        author1 = Author.objects.create(
            user=self.user, name='Tolkien'
        )
        author2 = Author.objects.create(
            user=self.user, name='Ghandi'
        )
        # Create book
        book = Book.objects.create(
            title='Cinderella',
            pages=100,
            year=1854,
            price=10,
            user=self.user
        )
        # Add autho to book
        book.authors.add(author1)

        # Make HTTP request to get authors assigned to at
        # least a book
        res = self.client.get(AUTHOR_URL, {'assigned_only': 1})

        # Get JSON for author objects
        serializer1 = AuthorSerializer(author1)
        serializer2 = AuthorSerializer(author2)
        # Check that only the first author is on the response
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_authors_assigned_unique(self):
        """Test filtering authors by assigned returns unique items"""
        # Create two authors
        author = Author.objects.create(user=self.user, name='Pablo Neruda')
        Author.objects.create(user=self.user, name='Fiona Barton')
        # Create books and add authors
        book1 = Book.objects.create(
            title='The Great Gatsby',
            pages=300,
            year=1974,
            price=12.00,
            user=self.user
        )
        book1.authors.add(author)
        book2 = Book.objects.create(
            title='Gulag',
            pages=243,
            year=1904,
            price=5.00,
            user=self.user
        )
        book2.authors.add(author)

        # Make HTTP request to get authors assigned to at least
        # one book
        res = self.client.get(AUTHOR_URL, {'assigned_only': 1})

        # Check that only one author is returned
        self.assertEqual(len(res.data), 1)
