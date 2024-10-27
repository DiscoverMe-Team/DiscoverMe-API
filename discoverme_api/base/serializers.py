from rest_framework import serializers
from .models import Mood,MoodLog, JournalEntry,Suggestion, Goal, Insight

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'mood_type', 'mood_description']  # Do not include 'user' field

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'mood_type', 'mood_description']  # Do not include 'user' field
class MoodLogSerializer(serializers.ModelSerializer):
    mood = MoodSerializer()  # Nesting MoodSerializer to show mood details
    
    class Meta:
        model = MoodLog
        fields = ['id', 'mood', 'date_logged', 'notes']

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


