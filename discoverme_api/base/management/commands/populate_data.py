import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import Mood, MoodLog, JournalEntry, Goal, Insight

MOODS = ['Happy', 'Sad', 'Angry', 'Calm', 'Anxious', 'Excited']
MOOD_DESCRIPTIONS = [
    "Feeling very happy and content.",
    "Feeling a bit down today.",
    "Angry about recent events.",
    "Calm and relaxed.",
    "Feeling anxious and nervous.",
    "Excited about upcoming plans."
]

GOAL_CATEGORIES = ['FIT', 'HABIT', 'EAT', 'SLEEP', 'STRESS', 'BAD', 'GROWTH']
GOAL_TITLES = [
    "Exercise Daily", "Drink More Water", "Sleep 8 Hours", "Meditate", "Read Books", "Reduce Screen Time"
]

INSIGHT_TRIGGERS = ['work', 'family', 'stress', 'exercise', 'sleep']

class Command(BaseCommand):
    help = 'Populate database with dummy data for testing.'

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_moods()
        self.create_mood_logs()
        self.create_journal_entries()
        self.create_goals()
        self.create_insights()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

    def create_users(self):
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
            self.stdout.write('Created test user.')

    def create_moods(self):
        for mood, description in zip(MOODS, MOOD_DESCRIPTIONS):
            if not Mood.objects.filter(mood_type=mood).exists():
                Mood.objects.create(mood_type=mood, mood_description=description)
        self.stdout.write('Created moods.')

    def create_mood_logs(self):
        user = User.objects.get(username='testuser')
        moods = list(Mood.objects.all())

        for _ in range(10):
            mood = random.choice(moods)
            date_logged = datetime.now() - timedelta(days=random.randint(0, 30))
            notes = random.choice(MOOD_DESCRIPTIONS)
            MoodLog.objects.create(user=user, mood=mood, date_logged=date_logged, notes=notes)

        self.stdout.write('Created mood logs.')

    def create_journal_entries(self):
        user = User.objects.get(username='testuser')

        for i in range(5):
            title = f"Journal Entry {i + 1}"
            content = f"This is the content of journal entry {i + 1}. It contains random thoughts and reflections."
            created_at = datetime.now() - timedelta(days=random.randint(0, 30))
            JournalEntry.objects.create(user=user, title=title, content=content, created_at=created_at)

        self.stdout.write('Created journal entries.')

    def create_goals(self):
        user = User.objects.get(username='testuser')

        for category, title in zip(GOAL_CATEGORIES, GOAL_TITLES):
            description = f"Goal to {title.lower()}."
            start_date = datetime.now() - timedelta(days=random.randint(0, 30))
            duration = random.randint(1, 12)
            duration_unit = random.choice(['DAYS', 'WEEKS', 'MONTHS'])
            Goal.objects.create(
                user=user,
                category=category,
                title=title,
                description=description,
                completed=random.choice([True, False]),
                start_date=start_date,
                times_per_day=random.randint(1, 3),
                days_per_week=random.randint(1, 7),
                duration=duration,
                duration_unit=duration_unit
            )

        self.stdout.write('Created goals.')

    def create_insights(self):
        user = User.objects.get(username='testuser')

        for trigger_word in INSIGHT_TRIGGERS:
            time_quantity = random.randint(1, 4)
            time_frame = random.choice(['days', 'weeks', 'months'])
            mood_count = random.randint(1, 20)
            created_at = datetime.now() - timedelta(days=random.randint(0, 30))
            Insight.objects.create(
                user=user,
                trigger_word=trigger_word,
                time_quantity=time_quantity,
                time_frame=time_frame,
                mood_count=mood_count,
                created_at=created_at
            )

        self.stdout.write('Created insights.')
