import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import Mood, MoodLog, JournalEntry, Goal, Insight

class Command(BaseCommand):
    """
    Django management command to populate the database with dummy data
    for testing purposes. This includes users, moods, mood logs, journal entries,
    goals, and insights.
    """
    help = 'Populate database with dummy data for testing.'

    def add_arguments(self, parser):
        """
        Add custom command-line arguments for controlling the number of records generated.

        :param parser: Argument parser for the command.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument('--num-moodlogs', type=int, default=10, help='Number of mood logs to create')
        parser.add_argument('--num-journalentries', type=int, default=5, help='Number of journal entries to create')
        parser.add_argument('--num-goals', type=int, default=6, help='Number of goals to create')
        parser.add_argument('--num-insights', type=int, default=5, help='Number of insights to create')

    def handle(self, *args, **kwargs):
        """
        Execute the command to populate the database with dummy data.

        :param args: Variable length argument list.
        :type args: list
        :param kwargs: Arbitrary keyword arguments for custom arguments.
        :type kwargs: dict
        """
        num_moodlogs = kwargs['num_moodlogs']
        num_journalentries = kwargs['num_journalentries']
        num_goals = kwargs['num_goals']
        num_insights = kwargs['num_insights']

        self.create_users()
        self.create_moods()
        self.create_mood_logs(num_moodlogs)
        self.create_journal_entries(num_journalentries)
        self.create_goals(num_goals)
        self.create_insights(num_insights)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

    def create_users(self):
        """
        Create test users if they do not already exist.

        :raises IntegrityError: If a user with the same username already exists.
        """
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
            self.stdout.write('Created test user.')

    def create_moods(self):
        """
        Create predefined moods in the database if they do not already exist.

        :raises IntegrityError: If a mood with the same type already exists.
        """
        created_count = 0
        moods = ['Happy', 'Sad', 'Angry', 'Calm', 'Anxious', 'Excited']
        descriptions = [
            "Feeling very happy and content.",
            "Feeling a bit down today.",
            "Angry about recent events.",
            "Calm and relaxed.",
            "Feeling anxious and nervous.",
            "Excited about upcoming plans."
        ]

        for mood, description in zip(moods, descriptions):
            if not Mood.objects.filter(mood_type=mood).exists():
                Mood.objects.create(mood_type=mood, mood_description=description)
                created_count += 1
        self.stdout.write(f'Created {created_count} moods.')

    def create_mood_logs(self, num):
        """
        Create dummy mood logs for the test user.

        :param num: The number of mood logs to create.
        :type num: int
        """
        user = User.objects.get(username='testuser')
        moods = list(Mood.objects.all())
        created_count = 0

        for _ in range(num):
            mood = random.choice(moods)
            date_logged = datetime.now() - timedelta(days=random.randint(0, 30))
            notes = random.choice([
                "Had a productive day.",
                "Feeling down today.",
                "Excited about tomorrow!",
                "Relaxed after a good workout."
            ])
            MoodLog.objects.create(user=user, mood=mood, date_logged=date_logged, notes=notes)
            created_count += 1

        self.stdout.write(f'Created {created_count} mood logs.')

    def create_journal_entries(self, num):
        """
        Create dummy journal entries for the test user.

        :param num: The number of journal entries to create.
        :type num: int
        """
        user = User.objects.get(username='testuser')
        created_count = 0

        for i in range(num):
            title = f"Journal Entry {i + 1}"
            content = f"This is the content of journal entry {i + 1}. It contains random thoughts and reflections."
            created_at = datetime.now() - timedelta(days=random.randint(0, 30))
            JournalEntry.objects.create(user=user, title=title, content=content, created_at=created_at)
            created_count += 1

        self.stdout.write(f'Created {created_count} journal entries.')

    def create_goals(self, num):
        """
        Create dummy goals for the test user.

        :param num: The number of goals to create.
        :type num: int
        """
        user = User.objects.get(username='testuser')
        created_count = 0

        for i in range(num):
            category = random.choice(['FIT', 'HABIT', 'EAT', 'SLEEP', 'STRESS', 'BAD', 'GROWTH'])
            title = f"Goal {i + 1}"
            description = f"This is a description for goal {i + 1}."
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
            created_count += 1

        self.stdout.write(f'Created {created_count} goals.')

    def create_insights(self, num):
        """
        Create dummy insights for the test user.

        :param num: The number of insights to create.
        :type num: int
        """
        user = User.objects.get(username='testuser')
        created_count = 0

        for _ in range(num):
            trigger_word = random.choice(['work', 'family', 'stress', 'exercise', 'sleep'])
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
            created_count += 1

        self.stdout.write(f'Created {created_count} insights.')
