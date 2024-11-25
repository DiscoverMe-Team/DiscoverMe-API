from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    CATEGORY_CHOICES = {
    'FIT': 'Get Fit',
    'HABIT': 'Build Good Habits',
    'EAT': 'Eat Healthier',
    'SLEEP': 'Better Sleep',
    'STRESS': 'Reduce Stress',
    'BAD': 'Break Bad Habits',
    'GROWTH': 'Self Growth',
    }

    DURATION_UNIT_CHOICES = [
        ('DAYS', 'Days'),
        ('WEEKS', 'Weeks'),
        ('MONTHS', 'Months'),
        ('YEARS', 'Years'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Self Growth')
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    times_per_day = models.PositiveBigIntegerField(default=1)
    days_per_week = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField(default=1, help_text="How long will this goal last?")
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default='WEEKS')

    def __str__(self):
        return f"{self.title} for {self.user.username}"

class Insight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trigger_word = models.CharField(max_length=50)  # Trigger word this insight is focused on
    time_quantity = models.PositiveIntegerField(default=1)
    time_frame = models.CharField(max_length=10, choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], default='weeks')
    mood_count = models.IntegerField(default=0)  # Count of trigger word occurrences
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mood Insight Trends for {self.user.username} on {self.trigger_word} over {self.time_frame}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    location = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()