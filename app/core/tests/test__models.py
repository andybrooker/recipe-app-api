from multiprocessing.sharedctypes import Value
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test__create_user_with_email__successful(self):
        '''Test creating a new user with an email is successful.'''
        email = 'test@test.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test__new_user_email_normalised(self):
        '''Test the email for a new user is normalized'''
        email = 'test@TEST.COM'

        user = get_user_model().objects.create_user(email)

        self.assertEqual(user.email, email.lower())

    def test__new_user_invalid_email(self):
        '''Test creating user with no email raises error'''
        with self.assertRaises(AssertionError):
            get_user_model().objects.create_user(None)

    def test__create_new_super_user(self):
        '''Test creates new super user'''
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
