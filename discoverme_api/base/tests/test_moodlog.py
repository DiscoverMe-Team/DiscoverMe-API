from rest_framework.test import APITestCase
from rest_framework import status
from ..models import MoodLog, Mood
from django.contrib.auth.models import User

class MoodLogTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.mood = Mood.objects.create(mood_type='Happy', mood_description='Feeling great')

    def test_create_moodlog(self):
        data = {'mood': self.mood.id, 'notes': 'Had a productive day'}
        response = self.client.post('/api/moodlogs/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_moodlog(self):
        moodlog = MoodLog.objects.create(user=self.user, mood=self.mood, notes='Good day')
        response = self.client.get(f'/api/moodlogs/{moodlog.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], 'Good day')
