from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Mood
from django.contrib.auth.models import User

class MoodTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword', email='admin@example.com')
        self.client.login(username='adminuser', password='adminpassword')  # Log in as an admin for create test

    def test_retrieve_mood(self):
        mood = Mood.objects.create(mood_type='Calm', mood_description='Feeling at peace')
        response = self.client.get(f'/api/mood/{mood.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mood_type'], 'Calm')
