from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book, Tag, Author

from book.serializers import BookSerializer, BookDetailSerializer


BOOKS_URL = reverse('book:book-list')


def detail_url(book_id):
    """Return book detail URL"""
    return reverse('book:book-detail', args=[book_id])


def sample_tag(user, name='Thriller'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_author(user, name='Pio Baroja'):
    """Create and return a sample author"""
    return Author.objects.create(user=user, name=name)


def sample_book(user, **params):
    """Create and return a sample book"""
    defaults = {
        'title': 'Sample book',
        'pages': 500,
        'year': 1984,
        'price': 5.00
    }
    # Update book attributes if specified on arguments
    defaults.update(params)

    # Return object created
    return Book.objects.create(user=user, **defaults)


class PublicBookApiTests(TestCase):
    """Test unauthenticated book API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        # Make HTTP request
        res = self.client.get(BOOKS_URL)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):
    """Test unauthenticated book API access"""

    def setUp(self):
        self.client = APIClient()
        # Create and authenticate user
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_books(self):
        """Test retrieving a list of books"""
        # Create two books
        sample_book(user=self.user)
        sample_book(user=self.user)

        # Make HTTP request to retrieve book list
        res = self.client.get(BOOKS_URL)

        # Get the books on the db
        books = Book.objects.all().order_by('-id')
        # Get the JSON
        serializer = BookSerializer(books, many=True)
        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that the data matches
        self.assertEqual(res.data, serializer.data)

    def test_books_limited_to_user(self):
        """Test retrieving books for user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'password123'
        )
        # Create one book with each user
        sample_book(user=user2)
        sample_book(user=self.user)

        # Make HTTP request to get book list
        res = self.client.get(BOOKS_URL)

        # Get books on the db created by user
        books = Book.objects.filter(user=self.user)
        # Get JSON
        serializer = BookSerializer(books, many=True)
        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that there is only one book on the lsit
        self.assertEqual(len(res.data), 1)
        # Check that the data matches
        self.assertEqual(res.data, serializer.data)

    def test_view_book_detail(self):
        """Test viewing a book detail"""
        # Create new book
        book = sample_book(user=self.user)
        # Add tag to book
        book.tags.add(sample_tag(user=self.user))
        # Add author to book
        book.authors.add(sample_author(user=self.user))

        # Get the get detail of books endpoint url
        url = detail_url(book.id)
        # Make HTTP request to get the book details
        res = self.client.get(url)

        # Get the JSON
        serializer = BookDetailSerializer(book)
        # Check that the response data and the JSON match
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_book(self):
        """Test creating book"""
        payload = {
            'title': 'Alice in Wonderland',
            'pages': 500,
            'year': 1984,
            'price': 5.00
        }

        # Make HTTP post request to create book
        res = self.client.post(BOOKS_URL, payload)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Get the book created from the db
        book = Book.objects.get(id=res.data['id'])
        # Check that all the attributes match between object
        # and response
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_create_book_with_tags(self):
        """Test creating a book with tags"""
        # Create tags
        tag1 = sample_tag(user=self.user, name='Realism')
        tag2 = sample_tag(user=self.user, name='History')
        # Create sample book
        payload = {
            'title': 'Withering heights',
            'tags': [tag1.id, tag2.id],
            'pages': 300,
            'year': 1892,
            'price': 20.00
        }

        # Make HTTP post request to create book
        res = self.client.post(BOOKS_URL, payload)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Get book created from the db
        book = Book.objects.get(id=res.data['id'])
        # Get tag list
        tags = book.tags.all()
        # Check that there are two tags and they match
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_book_with_authors(self):
        """Test creating book with authors"""
        # Create authors
        author1 = sample_author(user=self.user, name='Sally Rooney')
        author2 = sample_author(user=self.user, name='Oscar Wilde')
        payload = {
            'title': '1984',
            'authors': [author1.id, author2.id],
            'pages': 400,
            'year': 1992,
            'price': 7.00
        }

        # Make HTTP request to create sample books
        res = self.client.post(BOOKS_URL, payload)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Retrieve book created from db
        book = Book.objects.get(id=res.data['id'])
        # Get authors and check that they match
        authors = book.authors.all()
        self.assertEqual(authors.count(), 2)
        self.assertIn(author1, authors)
        self.assertIn(author2, authors)
