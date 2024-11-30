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
        Create multiple test users with first and last names and their profiles.
        """
        users_data = [
            {
                'username': 'testuser1',
                'password': 'password1',
                'email': 'testuser1@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'profile': {
                    'location': 'New York, USA',
                    'occupation': 'Software Engineer',
                    'city': 'New York',
                    'state': 'NY',
                    'pronouns': 'He/Him',
                }
            },
            {
                'username': 'testuser2',
                'password': 'password2',
                'email': 'testuser2@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'profile': {
                    'location': 'Los Angeles, USA',
                    'occupation': 'Graphic Designer',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'pronouns': 'She/Her',
                }
            },
            {
                'username': 'testuser3',
                'password': 'password3',
                'email': 'testuser3@example.com',
                'first_name': 'Alex',
                'last_name': 'Taylor',
                'profile': {
                    'location': 'Chicago, USA',
                    'occupation': 'Data Scientist',
                    'city': 'Chicago',
                    'state': 'IL',
                    'pronouns': 'They/Them',
                }
            },
        ]

        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=user_data['password'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                user.profile.location = user_data['profile']['location']
                user.profile.occupation = user_data['profile']['occupation']
                user.profile.city = user_data['profile']['city']
                user.profile.state = user_data['profile']['state']
                user.profile.pronouns = user_data['profile']['pronouns']
                user.profile.save()
                self.stdout.write(f'Created {user.first_name} {user.last_name} ({username}) and populated profile.')
            else:
                self.stdout.write(f'{username} already exists.')

    def create_moods(self):
        """
        Create predefined moods in the database if they do not already exist.
        """
        moods = [
            {'mood_type': 'Happy', 'description': 'Feeling very happy and content.'},
            {'mood_type': 'Sad', 'description': 'Feeling a bit down today.'},
            {'mood_type': 'Angry', 'description': 'Angry about recent events.'},
            {'mood_type': 'Calm', 'description': 'Calm and relaxed.'},
            {'mood_type': 'Anxious', 'description': 'Feeling anxious and nervous.'},
            {'mood_type': 'Excited', 'description': 'Excited about upcoming plans.'},
        ]

        created_count = 0
        for mood in moods:
            if not Mood.objects.filter(mood_type=mood['mood_type']).exists():
                Mood.objects.create(mood_type=mood['mood_type'], mood_description=mood['description'])
                created_count += 1
        self.stdout.write(f'Created {created_count} moods.')

    def create_mood_logs(self, num):
        """
        Create dummy mood logs for all test users.
        """
        users = User.objects.filter(username__startswith='testuser')
        moods = list(Mood.objects.all())
        if not moods:
            self.stdout.write(self.style.ERROR('No moods found. Run create_moods first.'))
            return

        total_created = 0
        for user in users:
            for _ in range(num):
                MoodLog.objects.create(
                    user=user,
                    mood=random.choice(moods),
                    date_logged=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=random.choice([
                        "Had a productive day.",
                        "Feeling down today.",
                        "Excited about tomorrow!",
                        "Relaxed after a good workout."
                    ])
                )
                total_created += 1

        self.stdout.write(f'Created {total_created} mood logs.')

    def create_journal_entries(self, num):
        """
        Create dummy journal entries for all test users.
        """
        users = User.objects.filter(username__startswith='testuser')
        total_created = 0

        for user in users:
            for i in range(num):
                JournalEntry.objects.create(
                    user=user,
                    title=f"Journal Entry {i + 1}",
                    content=f"This is the content of journal entry {i + 1}.",
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                total_created += 1

        self.stdout.write(f'Created {total_created} journal entries.')

    def create_goals(self, num):
        """
        Create dummy goals for all test users.
        """
        users = User.objects.filter(username__startswith='testuser')
        categories = ['FIT', 'HABIT', 'EAT', 'SLEEP', 'STRESS', 'BAD', 'GROWTH']
        total_created = 0

        for user in users:
            for i in range(num):
                Goal.objects.create(
                    user=user,
                    category=random.choice(categories),
                    title=f"Goal {i + 1}",
                    description=f"This is a description for goal {i + 1}.",
                    start_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    completed=random.choice([True, False]),
                    times_per_day=random.randint(1, 3),
                    days_per_week=random.randint(1, 7),
                    duration=random.randint(1, 12),
                    duration_unit=random.choice(['DAYS', 'WEEKS', 'MONTHS'])
                )
                total_created += 1

        self.stdout.write(f'Created {total_created} goals.')

    def create_insights(self, num):
        """
        Create dummy insights for all test users.
        """
        users = User.objects.filter(username__startswith='testuser')
        total_created = 0

        for user in users:
            for _ in range(num):
                Insight.objects.create(
                    user=user,
                    trigger_word=random.choice(['work', 'family', 'stress', 'exercise', 'sleep']),
                    time_quantity=random.randint(1, 4),
                    time_frame=random.choice(['days', 'weeks', 'months']),
                    mood_count=random.randint(1, 20),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                total_created += 1

        self.stdout.write(f'Created {total_created} insights.')
