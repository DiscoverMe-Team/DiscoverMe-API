from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import Suggestion, Task, Goal
from django.utils.timezone import now
from emails.messages import send_welcome_email, send_congrats_email

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

@receiver(post_save, sender=User)
def handle_user_created(sender, instance, created, **kwargs):
    """
    Handle actions when a user is created.
    """
    if created:
        print(f"New user created: {instance.username}")

        if hasattr(instance, 'profile') and instance.profile.first_login:
                additional_suggestions = [
                    "Plan your meals for the week.",
                    "Declutter your workspace.",
                    "Connect with a friend or loved one."
                ]
                # Create suggestions
                Suggestion.objects.bulk_create([
                    Suggestion(user=instance, text=text)
                    for text in additional_suggestions
                ])

                # Update first_login field
                instance.profile.first_login = False
                instance.profile.save()
                # Send a welcome email
                try:
                    send_welcome_email(instance)
                    print(f"Welcome email sent to {instance.email}")
                except Exception as e:
                    print(f"Failed to send email to {instance.email}: {str(e)}")

@receiver(pre_save, sender=Task)
def update_task_completed_on(sender, instance, **kwargs):
    """
    Updates the completed_on field when the completed status of a Task changes to True
    and sends a congratulatory email.
    """
    if instance.completed and not instance.completed_on:
        instance.completed_on = now()
        # Send congratulatory email
        try:
            send_congrats_email(instance.goal.user, f"{instance.text}")
            print(f"Congrats email sent for task: {instance.text}")
        except Exception as e:
            print(f"Failed to send congrats email for task: {instance.text}. Error: {str(e)}")


@receiver(pre_save, sender=Goal)
def update_goal_completed_on(sender, instance, **kwargs):
    """
    Updates the completed_on field when the completed status of a Goal changes to True
    and sends a congratulatory email.
    """
    if instance.completed and not instance.completed_on:
        instance.completed_on = now()
        # Send congratulatory email
        try:
            send_congrats_email(instance.user, f"{instance.title}")
            print(f"Congrats email sent for goal: {instance.title}")
        except Exception as e:
            print(f"Failed to send congrats email for goal: {instance.title}. Error: {str(e)}")
