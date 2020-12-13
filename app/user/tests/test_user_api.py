from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):
    """Test users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'anvi@gmail.com',
            'password': '12345',
            'name': 'test'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        """Test create user that already exist"""
        payload = {
            'email': 'dkkv0001@gmail.com',
            'password': '12345',
            'name': 'anvi9'
        }
        # first create the user
        create_user(**payload)
        # now try to create the same user
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password is too short"""
        payload = {
            'email': 'dkkv0001@gmail.com',
            'password': '1234',
            'name': 'anvi9'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    # From here we are using a different end point TOKEN_URL
    def test_create_token_for_user(self):
        """Test that a token is created for a user"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test that token is not created for invalid credentials"""
        payload = {
            'email': 'anvi@gmail.com',
            'password': 'wrong123',
            'name': 'karun'
        }
        create_user(email='anvi@gmail.com', password='anvi123')
        response = self.client.post(TOKEN_URL, payload)

        # check the token and response code
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
