from rest_framework import serializers
from .models import Mood, MoodLog, JournalEntry

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'mood_type', 'mood_description']  # Do not include 'user' field

class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ['id', 'mood', 'date_logged', 'notes']  # Do not include 'user' field

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'created_at']  # Do not include 'user' field
