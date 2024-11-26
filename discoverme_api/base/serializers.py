from rest_framework import serializers
from .models import Mood, MoodLog, JournalEntry, Suggestion, Goal, Insight, UserProfile

class MoodSerializer(serializers.ModelSerializer):
    """
    Serializer for the Mood model.
    """
    class Meta:
        model = Mood
        fields = ['id', 'mood_type', 'mood_description']


class MoodLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the MoodLog model.
    """
    mood = serializers.PrimaryKeyRelatedField(queryset=Mood.objects.all())  # Allows referencing an existing Mood by ID

    class Meta:
        model = MoodLog
        fields = ['id', 'mood', 'date_logged', 'notes']


class JournalEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the JournalEntry model.
    """
    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'created_at']


class SuggestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Suggestion model.
    """
    class Meta:
        model = Suggestion
        fields = ['id', 'mood_trigger', 'suggestion_text']


class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Goal model.
    """
    class Meta:
        model = Goal
        fields = [
            'id', 'user', 'category', 'title', 'description', 'completed', 
            'start_date', 'times_per_day', 'days_per_week', 
            'duration', 'duration_unit'
        ]


class InsightSerializer(serializers.ModelSerializer):
    """
    Serializer for the Insight model.
    """
    class Meta:
        model = Insight
        fields = [
            'id', 'user', 'trigger_word', 'time_quantity', 
            'time_frame', 'mood_count', 'created_at'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    class Meta:
        model = UserProfile
        fields = ['location', 'occupation', 'city', 'state', 'pronouns']
