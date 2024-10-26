from django.db import models
from django.contrib.auth.models import User
from .utils import calculate_gad7_score, calculate_phq9_score, calculate_perceived_stress_score

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)
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

class PHQ9(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responses = models.JSONField()  # Store responses to each question as JSON
    score = models.IntegerField(blank=True, null=True)  # Total score for the questionnaire
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate the score based on responses
        self.score = calculate_phq9_score(self.responses)
        super().save(*args, **kwargs)

class GAD7(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responses = models.JSONField()
    score = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.score = calculate_gad7_score(self.responses)
        super().save(*args, **kwargs)

class PerceivedStressScale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responses = models.JSONField()
    score = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.score = calculate_perceived_stress_score(self.responses)
        super().save(*args, **kwargs)