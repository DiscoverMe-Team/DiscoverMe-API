from rest_framework import serializers
from .models import Mood,MoodLog, JournalEntry,Suggestion, Goal, Insight

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'mood_type', 'mood_description']  # Do not include 'user' field
        
class MoodLogSerializer(serializers.ModelSerializer):
    mood = serializers.PrimaryKeyRelatedField(queryset=Mood.objects.all())     
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
        fields = ['id', 'user', 'category', 'title', 'description', 'completed', 
                  'start_date', 'times_per_day', 'days_per_week', 
                  'duration', 'duration_unit']

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ['id', 'user', 'trigger_word', 'time_quantity', 'time_frame', 'mood_count', 'created_at']


