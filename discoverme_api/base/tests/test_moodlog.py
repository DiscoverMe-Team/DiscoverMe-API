from rest_framework.test import APITestCase
from rest_framework import status
from ..models import MoodLog, Mood
from django.contrib.auth.models import User

class MoodLogTests(APITestCase):
    
    def setUp(self):
        """
        Set up a test user and a test mood.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='testuser', password='testpassword')
        self.mood = Mood.objects.create(mood_type='Happy', mood_description='Feeling great')
        self.moodlog_url = '/api/moodlogs/'

    def test_create_moodlog(self):
        """
        Test creating a mood log.
        """
        data = {'mood': self.mood.id, 'notes': 'Had a productive day'}
        response = self.client.post(self.moodlog_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MoodLog.objects.count(), 1)
        self.assertEqual(MoodLog.objects.first().notes, 'Had a productive day')

    def test_retrieve_moodlog(self):
        """
        Test retrieving a specific mood log by ID.
        """
        moodlog = MoodLog.objects.create(user=self.user, mood=self.mood, notes='Good day')
        response = self.client.get(f'{self.moodlog_url}{moodlog.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], 'Good day')

    def test_update_moodlog(self):
        """
        Test updating an existing mood log.
        """
        moodlog = MoodLog.objects.create(user=self.user, mood=self.mood, notes='Average day')
        data = {'mood': self.mood.id, 'notes': 'Updated to a great day'}
        response = self.client.put(f'{self.moodlog_url}{moodlog.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], 'Updated to a great day')

    def test_delete_moodlog(self):
        """
        Test deleting a mood log.
        """
        moodlog = MoodLog.objects.create(user=self.user, mood=self.mood, notes='To be deleted')
        response = self.client.delete(f'{self.moodlog_url}{moodlog.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MoodLog.objects.count(), 0)

    def test_list_moodlogs(self):
        """
        Test listing all mood logs for the authenticated user.
        """
        MoodLog.objects.create(user=self.user, mood=self.mood, notes='Day 1')
        MoodLog.objects.create(user=self.user, mood=self.mood, notes='Day 2')
        response = self.client.get(self.moodlog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_moodlog_access_by_other_user(self):
        """
        Test that a user cannot access another user's mood log.
        """
        moodlog = MoodLog.objects.create(user=self.other_user, mood=self.mood, notes='Private log')
        response = self.client.get(f'{self.moodlog_url}{moodlog.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_create_moodlog(self):
        """
        Test that an unauthenticated user cannot create a mood log.
        """
        self.client.logout()
        data = {'mood': self.mood.id, 'notes': 'Unauthorized log attempt'}
        response = self.client.post(self.moodlog_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access_moodlogs(self):
        """
        Test that an unauthenticated user cannot retrieve mood logs.
        """
        self.client.logout()
        response = self.client.get(self.moodlog_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
