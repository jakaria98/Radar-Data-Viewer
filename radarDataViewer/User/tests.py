from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_missing_username(self):
        response = self.client.post('/api/login/', {'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username and password are required', response.data['detail'])

    def test_missing_password(self):
        response = self.client.post('/api/login/', {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username and password are required', response.data['detail'])

    def test_invalid_credentials(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid credentials', response.data['detail'])

    def test_successful_login(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)


class RegisterViewTest(APITestCase):
    def test_successful_registration(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'password': 'securepassword',
            'email': 'newuser@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_invalid_data(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'password': '',
            'email': 'not-an-email',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data.get('email', []))


class UpdateUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


    def test_update_user_info(self):
        response = self.client.put('/api/update/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newemail@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], 'newemail@example.com')


    def test_update_password(self):
        response = self.client.put('/api/update/', {'password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        response = self.client.put('/api/update/', {'first_name': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_email(self):
        response = self.client.put('/api/update/', {'email': 'invalidemail'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
