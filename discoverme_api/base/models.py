from django.db import models
from django.contrib.auth.models import User

class Mood(models.Model):
    mood_type = models.CharField(max_length=10)
    mood_description = models.TextField()
    
    def __str__(self):
        return f'{self.mood_type}'

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.mood}'

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.user.username}'

class Suggestion(models.Model):
    mood_trigger = models.CharField(max_length=50)
    suggestion_text = models.TextField()

    def __str__(self):
        return f"Suggestion for {self.mood_trigger}"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"

class Insight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    most_frequent_mood = models.CharField(max_length=50, blank=True, null=True)
    mood_trend = models.JSONField()  # Store trends as a JSON object
    stress_related_entries_count = models.IntegerField(default=0)
    suggested_action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insight for {self.user.username} at {self.created_at}"

