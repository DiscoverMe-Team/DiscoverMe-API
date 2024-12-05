from rest_framework import serializers
from .models import Mood, MoodLog, JournalEntry, Suggestion, Goal, Insight, UserProfile, Task

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
        fields = ['id', 'user', 'text', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """
    class Meta:
        model = Task
        fields = ['id', 'goal', 'text', 'completed', 'completed_on']
        read_only_fields = ['goal', 'completed_on']  # Prevent modifications to `completed_on`

class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Goal model.
    Includes nested tasks.
    """
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = [
            'id', 'category', 'title', 'description', 'completed',
            'completed_on', 'start_date', 'times_per_day', 
            'days_per_week', 'duration', 'duration_unit', 'tasks'
        ]
        read_only_fields = ['completed_on']

class InsightSerializer(serializers.ModelSerializer):
    """
    Serializer for the Insight model.
    """
    class Meta:
        model = Insight
        fields = [
            'id', 'trigger_word', 'time_quantity', 
            'time_frame', 'mood_count', 'created_at'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    class Meta:
        model = UserProfile
        fields = ['location', 'occupation', 'city', 'state', 'pronouns']
