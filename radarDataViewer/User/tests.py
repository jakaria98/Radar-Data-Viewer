from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime
import os
import unittest
from .models import RadarFile, timestamped_file_path

class UserLoginValidationTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.valid_user = User.objects.create_user(
            username='validuser',
            password='validpassword'
        )

    # Case 1: valid username, valid password
    def test_login_valid_user_valid_password(self):
        user = authenticate(username='validuser', password='validpassword')
        self.assertIsNotNone(user, "User should be authenticated with valid username and password.")
        self.assertEqual(user.username, 'validuser', "The authenticated user should match the valid username.")

    # Case 2: invalid username, invalid password
    def test_login_invalid_user_invalid_password(self):
        user = authenticate(username='invaliduser', password='invalidpassword')
        self.assertIsNone(user, "Authentication should fail for invalid username and password.")

    # Case 3: invalid username, valid password
    def test_login_invalid_user_valid_password(self):
        user = authenticate(username='invaliduser', password='validpassword')
        self.assertIsNone(user, "Authentication should fail for invalid username and valid password.")

    # Case 4: valid username, invalid password
    def test_login_valid_user_invalid_password(self):
        user = authenticate(username='validuser', password='invalidpassword')
        self.assertIsNone(user, "Authentication should fail for valid username and invalid password.")

    def test_login_empty_fields(self):
    # Case 5: Empty username, valid password
    user = authenticate(username='', password='validpassword')
    self.assertIsNone(user, "Authentication should fail when username is empty.")

    # Case 6: Valid username, empty password
    user = authenticate(username='validuser', password='')
    self.assertIsNone(user, "Authentication should fail when password is empty.")

    # Case 7: Both fields are empty
    user = authenticate(username='', password='')
    self.assertIsNone(user, "Authentication should fail when both username and password are empty.")            

# filepath empty
# header empty
#
#
#
