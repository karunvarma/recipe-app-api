from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating with new user is successfull"""
        email = 'anvi@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        email = 'anvi@GMAIL.com'
        user = get_user_model().objects.create_user(email, password='test123')
        self.assertEqual(user.email, email.lower())

    def test_raise_exception_when_email_not_provided(self):
        '''Test to check whether is raised when email is not provied'''
        with self.assertRaises(ValueError):
            user = get_user_model()
            user.objects.create_user(email=None, password='test123')

    def test_create_new_super_user(self):
        '''Test creating a new super user'''
        user = get_user_model().objects.create_superuser(
            'anvi@gmail.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
