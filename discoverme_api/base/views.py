from rest_framework import viewsets
from .models import Mood, MoodLog, JournalEntry, Suggestion, Goal, Insight
from .serializers import MoodSerializer, MoodLogSerializer, JournalEntrySerializer, SuggestionSerializer, GoalSerializer, InsightSerializer
from rest_framework.permissions import IsAuthenticated

class MoodViewSet(viewsets.ModelViewSet):
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mood.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
        

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

class SuggestionViewSet(viewsets.ModelViewSet):
    serializer_class = SuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_moods = MoodLog.objects.filter(user=self.request.user).values_list('mood', flat=True)
        return Suggestion.objects.filter(mood_trigger__in=user_moods)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InsightViewSet(viewsets.ModelViewSet):
    serializer_class = InsightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Insight.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
