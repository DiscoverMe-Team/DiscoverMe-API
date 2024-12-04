from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Mood(models.Model):
    """
    Represents a type of mood and its description.

    :param mood_type: Short name or label for the mood (e.g., "Happy", "Sad").
    :type mood_type: str
    :param mood_description: Detailed description of the mood.
    :type mood_description: str
    """
    mood_type = models.CharField(max_length=10)
    mood_description = models.TextField()

    def __str__(self):
        return f'{self.mood_type}'


class MoodLog(models.Model):
    """
    Logs the user's mood at a specific date and time with optional notes.

    :param user: The user associated with the mood log.
    :type user: User
    :param mood: The mood being logged.
    :type mood: Mood
    :param date_logged: The timestamp of when the mood was logged.
    :type date_logged: datetime
    :param notes: Additional notes related to the logged mood.
    :type notes: str
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.mood}'


class JournalEntry(models.Model):
    """
    Represents a user's journal entry with a title, content, and timestamp.

    :param user: The user who created the journal entry.
    :type user: User
    :param title: Title of the journal entry.
    :type title: str
    :param content: Content of the journal entry.
    :type content: str
    :param created_at: The timestamp of when the entry was created.
    :type created_at: datetime
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.user.username}'
    
class Suggestion(models.Model):
    """
    Provides suggestions based on mood triggers.

    :param mood_trigger: The trigger word associated with the suggestion.
    :type mood_trigger: str
    :param suggestion_text: The suggestion provided for the trigger.
    :type suggestion_text: str
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    text = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.mood_trigger}"


class Goal(models.Model):
    """
    Represents a user's goal with categories, frequency, and duration details.

    :param user: The user who created the goal.
    :type user: User
    :param category: The category of the goal.
    :type category: str
    :param title: Title of the goal.
    :type title: str
    :param description: Detailed description of the goal.
    :type description: str
    :param completed: Status indicating if the goal is completed.
    :type completed: bool
    :param start_date: The timestamp when the goal was created.
    :type start_date: datetime
    :param times_per_day: Frequency of goal activities per day.
    :type times_per_day: int
    :param days_per_week: Frequency of goal activities per week.
    :type days_per_week: int
    :param duration: Duration of the goal.
    :type duration: int
    :param duration_unit: The unit of time for the duration (e.g., "Weeks").
    :type duration_unit: str
    """
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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GROWTH')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    times_per_day = models.PositiveBigIntegerField(default=1)
    days_per_week = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField(default=1)
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default='WEEKS')

    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.category}) for {self.user.username}"

class Task(models.Model):
    """
    Represents a task associated with a specific goal.

    Tasks are individual actionable items that belong to a goal. Each task 
    has a description, completion status, and a relationship with the parent goal.

    :param goal: The goal to which this task belongs.
    :type goal: Goal
    :param text: A short description of the task.
    :type text: str
    :param completed: Indicates whether the task has been completed.
    :type completed: bool
    """
    goal = models.ForeignKey(Goal, related_name='tasks', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the task, including its completion status.

        :return: A string describing the task and its completion status.
        :rtype: str
        """
        return f"Task: {self.text} (Completed: {self.completed})"

class Insight(models.Model):
    """
    Represents trends and insights based on user moods over time.

    :param user: The user associated with the insights.
    :type user: User
    :param trigger_word: The word triggering the insight.
    :type trigger_word: str
    :param time_quantity: The quantity of the time frame for the insight.
    :type time_quantity: int
    :param time_frame: The time unit (e.g., "Weeks") for the insight.
    :type time_frame: str
    :param mood_count: Count of moods matching the insight criteria.
    :type mood_count: int
    :param created_at: The timestamp when the insight was created.
    :type created_at: datetime
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trigger_word = models.CharField(max_length=50)
    time_quantity = models.PositiveIntegerField(default=1)
    time_frame = models.CharField(
        max_length=10,
        choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')],
        default='weeks'
    )
    mood_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mood Insight Trends for {self.user.username} on {self.trigger_word} over {self.time_frame}"


class UserProfile(models.Model):
    """
    Extends the default User model with additional fields.

    :param user: The related user.
    :type user: User
    :param location: The user's location.
    :type location: str
    :param occupation: The user's occupation.
    :type occupation: str
    :param city: The user's city.
    :type city: str
    :param state: The user's state.
    :type state: str
    :param pronouns: The user's pronouns.
    :type pronouns: str
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    location = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True, null=True)
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a UserProfile instance when a User is created.

    :param sender: The model class that triggered the signal.
    :param instance: The instance of the User model.
    :param created: A boolean indicating whether a new User was created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile whenever the associated User is saved.

    :param sender: The model class that triggered the signal.
    :param instance: The instance of the User model.
    """
    instance.profile.save()
