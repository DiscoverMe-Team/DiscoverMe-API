from rest_framework import serializers
from .models import MoodLog, JournalEntry

class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ['id', 'mood', 'date_logged', 'notes']  # Do not include 'user' field

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'created_at']  # Do not include 'user' field