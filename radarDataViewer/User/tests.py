from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_missing_username(self):
        response = self.client.post('/login/', {'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username and password are required', response.data['detail'])

    def test_missing_password(self):
        response = self.client.post('/login/', {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username and password are required', response.data['detail'])

    def test_invalid_credentials(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid credentials', response.data['detail'])

    def test_successful_login(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Login successful', response.data['message'])
