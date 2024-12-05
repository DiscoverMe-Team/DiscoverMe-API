from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import Suggestion, Task, Goal
from django.utils.timezone import now

@receiver(post_save, sender=User)
def generate_suggestions_for_new_user(sender, instance, created, **kwargs):
    """
    Generate default suggestions for a newly created user.
    """
    if created:
        # List of default suggestions
        default_suggestions = [
            "Create a goal: Go for a walk.",
            "Journal how your day is going.",
            "Watch a guided meditation video.",
            "Take a 5-minute stretch break.",
            "Write down 3 things you're grateful for."
        ]

        # Create suggestions for the new user
        Suggestion.objects.bulk_create([
            Suggestion(user=instance, text=text)
            for text in default_suggestions
        ])
        print(f"Suggestions created for user: {instance.username}")

@receiver(user_logged_in)
def handle_first_login(sender, request, user, **kwargs):
    """
    Handle first login for the user.
    """
    if user.profile.first_login:
        # Generate additional suggestions
        additional_suggestions = [
            "Plan your meals for the week.",
            "Declutter your workspace.",
            "Connect with a friend or loved one."
        ]
        Suggestion.objects.bulk_create([
            Suggestion(user=user, text=text)
            for text in additional_suggestions
        ])
        
        # Mark first_login as False
        user.profile.first_login = False
        user.profile.save()
        print(f"Suggestions generated for first login: {user.username}")

@receiver(pre_save, sender=Task)
def update_task_completed_on(sender, instance, **kwargs):
    """
    Updates the completed_on field when the completed status of a Task changes to True.
    """
    if instance.completed and not instance.completed_on:
        instance.completed_on = now()


@receiver(pre_save, sender=Goal)
def update_goal_completed_on(sender, instance, **kwargs):
    """
    Updates the completed_on field when the completed status of a Goal changes to True.
    """
    if instance.completed and not instance.completed_on:
        instance.completed_on = now()