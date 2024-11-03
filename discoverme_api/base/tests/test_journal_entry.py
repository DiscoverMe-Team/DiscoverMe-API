from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..models import JournalEntry

class JournalEntryTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='journaluser', password='testpassword')
        self.client.login(username='journaluser', password='testpassword')
        self.journal_entry_url = '/api/journalentries/'

    def test_create_journal_entry(self):
        data = {
            'title': 'My First Journal Entry',
            'content': 'Today was a productive day filled with coding and learning.'
        }
        response = self.client.post(self.journal_entry_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'My First Journal Entry')

    def test_retrieve_journal_entry(self):
        journal_entry = JournalEntry.objects.create(user=self.user, title='Sample Entry', content='Sample content.')
        response = self.client.get(f'{self.journal_entry_url}{journal_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Entry')

    def test_update_journal_entry(self):
        journal_entry = JournalEntry.objects.create(user=self.user, title='Old Title', content='Old content.')
        data = {'title': 'Updated Title', 'content': 'Updated content.'}
        response = self.client.put(f'{self.journal_entry_url}{journal_entry.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_journal_entry(self):
        journal_entry = JournalEntry.objects.create(user=self.user, title='Entry to Delete', content='This will be deleted.')
        response = self.client.delete(f'{self.journal_entry_url}{journal_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
