from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Mood
from django.contrib.auth.models import User

class MoodTests(APITestCase):

    def setUp(self):
        """
        Set up test users and authenticate an admin user for mood creation.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword', email='admin@example.com')
        self.client.login(username='adminuser', password='adminpassword')  # Log in as an admin for create test
        self.mood_url = '/api/mood/'  # Base URL for mood API

    def test_create_mood(self):
        """
        Test that an admin user can create a mood.
        """
        data = {'mood_type': 'Happy', 'mood_description': 'Feeling joyful and content'}
        response = self.client.post(self.mood_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['mood_type'], 'Happy')
        self.assertEqual(Mood.objects.count(), 1)

    def test_retrieve_mood(self):
        """
        Test retrieving a specific mood by ID.
        """
        mood = Mood.objects.create(mood_type='Calm', mood_description='Feeling at peace')
        response = self.client.get(f'{self.mood_url}{mood.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mood_type'], 'Calm')

    def test_update_mood(self):
        """
        Test updating an existing mood as an admin.
        """
        mood = Mood.objects.create(mood_type='Sad', mood_description='Feeling down')
        data = {'mood_type': 'Content', 'mood_description': 'Feeling satisfied'}
        response = self.client.put(f'{self.mood_url}{mood.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mood_type'], 'Content')
        self.assertEqual(response.data['mood_description'], 'Feeling satisfied')

    def test_delete_mood(self):
        """
        Test deleting a mood as an admin.
        """
        mood = Mood.objects.create(mood_type='Angry', mood_description='Feeling irritable')
        response = self.client.delete(f'{self.mood_url}{mood.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mood.objects.count(), 0)

    def test_list_moods(self):
        """
        Test listing all moods.
        """
        Mood.objects.create(mood_type='Excited', mood_description='Feeling thrilled')
        Mood.objects.create(mood_type='Relaxed', mood_description='Feeling calm and at ease')
        response = self.client.get(self.mood_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthorized_create_mood(self):
        """
        Test that a non-admin user cannot create a mood.
        """
        self.client.logout()  # Log out admin
        self.client.login(username='testuser', password='testpassword')  # Log in as regular user
        data = {'mood_type': 'Happy', 'mood_description': 'Feeling joyful and content'}
        response = self.client.post(self.mood_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update_mood(self):
        """
        Test that a non-admin user cannot update a mood.
        """
        mood = Mood.objects.create(mood_type='Stressed', mood_description='Feeling overwhelmed')
        self.client.logout()  # Log out admin
        self.client.login(username='testuser', password='testpassword')  # Log in as regular user
        data = {'mood_type': 'Chill', 'mood_description': 'Feeling relaxed'}
        response = self.client.put(f'{self.mood_url}{mood.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete_mood(self):
        """
        Test that a non-admin user cannot delete a mood.
        """
        mood = Mood.objects.create(mood_type='Frustrated', mood_description='Feeling annoyed')
        self.client.logout()  # Log out admin
        self.client.login(username='testuser', password='testpassword')  # Log in as regular user
        response = self.client.delete(f'{self.mood_url}{mood.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
