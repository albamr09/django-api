from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Helper function to create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@email.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EMAIL.com'
        user = get_user_model().objects.create_user(email, 'pass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        # Create the tag object
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Horror'
        )

        # Converting the tag object to string gives the tag name
        self.assertEqual(str(tag), tag.name)

    def test_author_str(self):
        """Test the author string representation"""
        # Create the tag object
        author = models.Author.objects.create(
            user=sample_user(),
            name='Edgar Alla Poe'
        )

        # Converting the tag object to string gives the tag name
        self.assertEqual(str(author), author.name)

    def test_book_str(self):
        """Test the book string representation"""
        book = models.Book.objects.create(
            user=sample_user(),
            title='Crime and Punishment',
            pages=500,
            year=1866,
            price=21.99,
        )

        self.assertEqual(str(book), book.title)

    @patch('uuid.uuid4')
    def test_book_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        # Change the return value of the uuid function
        # so it return 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.book_image_file_path(None, 'myimage.jpg')

        # Define expected path with literal string interpolation
        exp_path = f'uploads/book/{uuid}.jpg'
        # Check that the path match
        self.assertEqual(file_path, exp_path)
