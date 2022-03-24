from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    '''Test the users API (public)'''

    def setUp(self):
        self.client = APIClient()
    
    def test__create_valid_user_success_returns_valid_payload(self):
        '''Test creating user with valid payload is successful.'''

        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'Test'
        }
        
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test__create_user__user_already_exists(self):
        '''Test creating user that already exists fails.'''

        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'Test'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test__user_password_to_short(self):
        '''Test that the password is more than 5 characters.'''

        payload = {
            'email': 'test@test.com',
            'password': 'test',
            'name': 'Test'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test__create_token_for_user(self):
        '''Test that a token is created for the user.'''
        payload = {'email': 'test@test.com', 'password':'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test__create_token_invalid_credentials(self):
        '''Test that token is not created if invalid credentials are given.'''
        create_user(email='test@test.com', password='testpass')
        payload = {'email':'test@test.com', 'password':'wrongpass'}    
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test__create_token_no_user(self):
        '''Test that the token is not created if user doesn't exist.'''
    
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test__create_token_field_missing(self):
        '''Test that email and password are required.'''
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)