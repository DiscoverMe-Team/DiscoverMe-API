from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class TokenAuthTests(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = '/api/token/'
        self.refresh_url = '/api/token/refresh/'
        self.moodlog_url = '/api/moodlogs/'

    def test_obtain_token(self):
        # Test obtaining an access and refresh token
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_protected_view_with_token(self):
        # Obtain the token first
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = response.data['access']

        # Access a protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        protected_response = self.client.get(self.moodlog_url)
        
        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

    def test_expired_access_token(self):
        # Simulate using an expired token (handled in real testing with token manipulation or mocking)
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(seconds=-1)) # Simulate expiration
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(access_token)}')
        response = self.client.get(self.moodlog_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        # Obtain the initial refresh token
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        refresh_token = response.data['refresh']

        # Use the refresh token to get a new access token
        refresh_response = self.client.post(self.refresh_url, {
            'refresh': refresh_token
        })
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_invalid_refresh_token(self):
        # Test using an invalid or expired refresh token
        invalid_refresh_token = 'invalidtoken'
        response = self.client.post(self.refresh_url, {
            'refresh': invalid_refresh_token
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_view_without_token(self):
        # Attempt to access a protected view without a token
        response = self.client.get(self.moodlog_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_with_invalid_credentials(self):
        # Test obtaining a token with incorrect credentials
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_refresh_token(self):
        # Simulate using an expired refresh token
        refresh = RefreshToken.for_user(self.user)
        refresh.set_exp(lifetime=timedelta(seconds=-1))  # Simulate expiration
        
        response = self.client.post(self.refresh_url, {
            'refresh': str(refresh)
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
