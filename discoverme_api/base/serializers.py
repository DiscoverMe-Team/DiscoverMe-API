from rest_framework import serializers
from .models import MoodLog, JournalEntry, Suggestion, Goal

class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ['id', 'mood', 'date_logged', 'notes']  # Do not include 'user' field

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'created_at']  # Do not include 'user' field

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['id', 'mood_trigger', 'suggestion_text']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'due_date']

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ['id', 'most_frequent_mood', 'mood_trend', 'stress_related_entries_count', 'suggested_action', 'created_at']

class PHQ9Serializer(serializers.ModelSerializer):
    class Meta:
        model = PHQ9
        fields = ['id', 'user', 'responses', 'score', 'created_at']

class GAD7Serializer(serializers.ModelSerializer):
    class Meta:
        model = GAD7
        fields = ['id', 'user', 'responses', 'score', 'created_at']

class PerceivedStressScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerceivedStressScale
        fields = ['id', 'user', 'responses', 'score', 'created_at']
