from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..models import JournalEntry

class JournalEntryTests(APITestCase):

    def setUp(self):
        """
        Setup test data: create a test user and log in.
        """
        self.user = User.objects.create_user(username='journaluser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='journaluser', password='testpassword')
        self.journal_entry_url = '/api/journalentries/'

    def test_create_journal_entry(self):
        """
        Test the creation of a journal entry.
        """
        data = {
            'title': 'My First Journal Entry',
            'content': 'Today was a productive day filled with coding and learning.'
        }
        response = self.client.post(self.journal_entry_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'My First Journal Entry')
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_retrieve_journal_entry(self):
        """
        Test retrieving a specific journal entry by ID.
        """
        journal_entry = JournalEntry.objects.create(user=self.user, title='Sample Entry', content='Sample content.')
        response = self.client.get(f'{self.journal_entry_url}{journal_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Entry')

    def test_update_journal_entry(self):
        """
        Test updating an existing journal entry.
        """
        journal_entry = JournalEntry.objects.create(user=self.user, title='Old Title', content='Old content.')
        data = {'title': 'Updated Title', 'content': 'Updated content.'}
        response = self.client.put(f'{self.journal_entry_url}{journal_entry.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_journal_entry(self):
        """
        Test deleting a journal entry.
        """
        journal_entry = JournalEntry.objects.create(user=self.user, title='Entry to Delete', content='This will be deleted.')
        response = self.client.delete(f'{self.journal_entry_url}{journal_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(JournalEntry.objects.count(), 0)

    def test_unauthorized_access(self):
        """
        Test that unauthorized users cannot access journal entries.
        """
        journal_entry = JournalEntry.objects.create(user=self.user, title='Private Entry', content='Not for others.')
        self.client.logout()
        response = self.client.get(f'{self.journal_entry_url}{journal_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_other_user_journal_entry(self):
        """
        Test that users cannot access journal entries of other users.
        """
        journal_entry = JournalEntry.objects.create(user=self.other_user, title='Other User Entry', content='Not yours!')
        response = self.client.get(f'{self.journal_entry_url}{journal_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_create_journal_entry(self):
        """
        Test creating a journal entry with invalid data.
        """
        data = {'title': '', 'content': ''}
        response = self.client.post(self.journal_entry_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
