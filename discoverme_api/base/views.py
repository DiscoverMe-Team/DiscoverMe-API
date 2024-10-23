from rest_framework import viewsets
from .models import MoodLog, JournalEntry
from .serializers import MoodLogSerializer, JournalEntrySerializer
from rest_framework.permissions import IsAuthenticated

class MoodLogViewSet(viewsets.ModelViewSet):
    serializer_class = MoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return mood logs for the authenticated user
        return MoodLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the created mood log with the logged-in user
        serializer.save(user=self.request.user)

class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return journal entries for the authenticated user
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the created journal entry with the logged-in user
        serializer.save(user=self.request.user)
