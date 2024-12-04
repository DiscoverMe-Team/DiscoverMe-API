import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import Mood, MoodLog, JournalEntry, Goal, Insight, Suggestion, Task

class Command(BaseCommand):
    """
    Django management command to populate the database with realistic dummy data
    for testing purposes. Includes users, moods, mood logs, journal entries,
    goals, tasks, insights, and suggestions.
    """
    help = 'Populate the database with realistic dummy data for testing.'

    def add_arguments(self, parser):
        """
        Add custom command-line arguments for controlling the number of records generated.
        """
        parser.add_argument('--num-moodlogs', type=int, default=10, help='Number of mood logs to create')
        parser.add_argument('--num-journalentries', type=int, default=5, help='Number of journal entries to create')
        parser.add_argument('--num-goals', type=int, default=6, help='Number of goals to create')
        parser.add_argument('--num-tasks-per-goal', type=int, default=3, help='Number of tasks per goal to create')
        parser.add_argument('--num-insights', type=int, default=5, help='Number of insights to create')
        parser.add_argument('--num-suggestions', type=int, default=10, help='Number of suggestions to create')

    def handle(self, *args, **kwargs):
        """
        Execute the command to populate the database with dummy data.
        """
        num_moodlogs = kwargs['num_moodlogs']
        num_journalentries = kwargs['num_journalentries']
        num_goals = kwargs['num_goals']
        num_tasks_per_goal = kwargs['num_tasks_per_goal']
        num_insights = kwargs['num_insights']
        num_suggestions = kwargs['num_suggestions']

        self.create_users()
        self.create_moods()
        self.create_mood_logs(num_moodlogs)
        self.create_journal_entries(num_journalentries)
        self.create_goals_and_tasks(num_goals, num_tasks_per_goal)
        self.create_insights(num_insights)
        self.create_suggestions(num_suggestions)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with realistic dummy data.'))

    def create_users(self):
        """
        Create realistic test users with profile data.
        """
        users_data = [
            {
                'username': 'emilyw',
                'password': 'securepassword1',
                'email': 'emily.williams@example.com',
                'first_name': 'Emily',
                'last_name': 'Williams',
                'profile': {
                    'location': 'New York, USA',
                    'occupation': 'Marketing Manager',
                    'city': 'New York',
                    'state': 'NY',
                    'pronouns': 'She/Her',
                }
            },
            {
                'username': 'johnd',
                'password': 'securepassword2',
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'profile': {
                    'location': 'San Francisco, USA',
                    'occupation': 'Software Developer',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'pronouns': 'He/Him',
                }
            },
            {
                'username': 'alex_t',
                'password': 'securepassword3',
                'email': 'alex.taylor@example.com',
                'first_name': 'Alex',
                'last_name': 'Taylor',
                'profile': {
                    'location': 'Chicago, USA',
                    'occupation': 'UX Designer',
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
                user.profile.first_login = False
                user.profile.save()
                self.stdout.write(f'Created user: {user.first_name} {user.last_name} ({username}).')

    def create_moods(self):
        """
        Create predefined moods.
        """
        moods = [
            {'mood_type': 'happy', 'description': 'Feeling joyful and satisfied.'},
            {'mood_type': 'stressed', 'description': 'Overwhelmed by tasks and deadlines.'},
            {'mood_type': 'relaxed', 'description': 'Feeling calm and at ease.'},
            {'mood_type': 'motivated', 'description': 'Eager to tackle challenges.'},
            {'mood_type': 'tired', 'description': 'Lacking energy and feeling drained.'},
        ]

        for mood in moods:
            Mood.objects.get_or_create(mood_type=mood['mood_type'], mood_description=mood['description'])

    def create_mood_logs(self, num):
        """
        Create mood logs for all users.
        """
        users = User.objects.all()
        moods = list(Mood.objects.all())
        for user in users:
            for _ in range(num):
                MoodLog.objects.create(
                    user=user,
                    mood=random.choice(moods),
                    date_logged=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=random.choice([
                        "Had a productive meeting at work.",
                        "Struggled with focus today.",
                        "Enjoyed a peaceful walk in the park.",
                        "Feeling positive after accomplishing a task."
                    ])
                )

    def create_journal_entries(self, num):
        """
        Create journal entries for all users.
        """
        users = User.objects.all()
        for user in users:
            for _ in range(num):
                JournalEntry.objects.create(
                    user=user,
                    title=f"Reflection on {datetime.now().strftime('%A')}",
                    content=random.choice([
                        "Today was a great day! I managed to complete my tasks and had time to relax.",
                        "Feeling overwhelmed but also learned something new at work.",
                        "Spent quality time with friends, which helped improve my mood."
                    ]),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30))
                )

    def create_goals_and_tasks(self, num_goals, num_tasks):
        """
        Create goals and their associated tasks.
        """
        users = User.objects.all()
        categories = ['Health', 'Career', 'Personal Development', 'Relationships', 'Fitness']
        for user in users:
            for i in range(num_goals):
                goal = Goal.objects.create(
                    user=user,
                    category=random.choice(categories),
                    title=f"Goal {i + 1}: {random.choice(['Improve fitness', 'Read more books', 'Learn a new skill'])}",
                    description=f"Work on personal development by achieving {i + 1} milestones.",
                    start_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    completed=random.choice([True, False]),
                    times_per_day=random.randint(1, 2),
                    days_per_week=random.randint(1, 7),
                    duration=random.randint(1, 12),
                    duration_unit=random.choice(['Days', 'Weeks', 'Months'])
                )

                for j in range(num_tasks):
                    Task.objects.create(
                        goal=goal,
                        text=f"Task {j + 1} for {goal.title}",
                        completed=random.choice([True, False])
                    )

    def create_insights(self, num):
        """
        Create insights for all users.
        """
        users = User.objects.all()
        for user in users:
            for _ in range(num):
                Insight.objects.create(
                    user=user,
                    trigger_word=random.choice(['stress', 'exercise', 'focus', 'happiness', 'relationships']),
                    time_quantity=random.randint(1, 4),
                    time_frame=random.choice(['days', 'weeks']),
                    mood_count=random.randint(1, 10),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30))
                )

    def create_suggestions(self, num):
        """
        Create suggestions for all users.
        """
        users = User.objects.all()
        suggestion_texts = [
            "Create a goal: Go for a walk.",
            "Journal how your day is going.",
            "Watch a guided meditation video.",
            "Take a 5-minute stretch break.",
            "Write down 3 things you're grateful for.",
            "Plan your meals for the week.",
            "Spend 10 minutes reading a book.",
            "Do a breathing exercise for 2 minutes.",
            "Declutter your workspace.",
            "Connect with a friend or loved one.",
        ]

        for user in users:
            for _ in range(num):
                Suggestion.objects.create(
                    user=user,
                    text=random.choice(suggestion_texts),
                    completed=random.choice([True, False])
                )
