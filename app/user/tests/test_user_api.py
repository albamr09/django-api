from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# Create user api endpoint dinamically
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# Helper function
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        # Send post request to create user
        res = self.client.post(CREATE_USER_URL, payload)

        # Check the status http code from the response
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Obtain the user object from the response data
        user = get_user_model().objects.get(**res.data)
        # Check that the users pass and the payload's pass are the same
        self.assertTrue(user.check_password(payload['password']))
        # Check that the pass is not contained within the response
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creatinga  user that already exists fails"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass',
            'name': 'Test',
        }

        # Create the user with the helper function
        create_user(**payload)

        # Make a post request to create the same user
        res = self.client.post(CREATE_USER_URL, payload)

        # Check that we get an error because the user already exists
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@email.com',
            'password': 'pw',
            'name': 'Test',
        }

        # Create user
        res = self.client.post(CREATE_USER_URL, payload)

        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the user we wanted to create is on the database
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # Check that is does not exist
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@email.com', 'password': 'testpass'}
        # Create the user in the db
        create_user(**payload)
        # Make post request to retrieve api token
        res = self.client.post(TOKEN_URL, payload)

        # Check that the response includes a key called token
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        # Create the user in the db
        create_user(email='test@email.com', password="testpass")
        payload = {'email': 'test@email.com', 'password': 'wrong'}
        # Make post request to retrieve api token
        res = self.client.post(TOKEN_URL, payload)

        # Check that the response does no include the api token
        self.assertNotIn('token', res.data)
        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@email.com', 'password': 'testpass'}
        # Make post request to retrieve api token
        res = self.client.post(TOKEN_URL, payload)

        # Check there response does not contain the token key
        self.assertNotIn('token', res.data)
        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        # Make post request to retrieve api token
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        # Check there response does not contain the token key
        self.assertNotIn('token', res.data)
        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        # Make HTTP get request to private endpoint unauthorized
        res = self.client.get(ME_URL)

        # Check that the requeset failed with unauthorized status
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        """ Helper function to create and authenticate user requests"""
        self.user = create_user(
            email='test@email.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        # Make request (user already authenticated on the setup)
        res = self.client.get(ME_URL)

        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that the data coincedes
        # NOTE: do not put password in plain text, use user object
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        # Make post request
        res = self.client.post(ME_URL, {})

        # Check that the request failed
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        # Make patch request to modify user
        res = self.client.patch(ME_URL, payload)

        # Update user values on db
        self.user.refresh_from_db()
        # Check that the password and the user have changed
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        # Check that the request was successfull
        self.assertEqual(res.status_code, status.HTTP_200_OK)
